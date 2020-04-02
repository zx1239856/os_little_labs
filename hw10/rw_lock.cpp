#include <unistd.h>
#include <iostream>
#include <iomanip>
#include <string>
#include <condition_variable>
#include <mutex>
#include <vector>
#include <thread>

// Since Semaphore is unavailable before C++20, it is better to craft it by hand
class Semaphore
{
public:
    explicit Semaphore(int count = 0) : _count(count) {}

    inline void signal()
    {
        std::unique_lock<std::mutex> lock(_mtx);
        _count++;
        _cv.notify_one();
    }
    inline void wait()
    {
        std::unique_lock<std::mutex> lock(_mtx);
        while (_count == 0)
        {
            _cv.wait(lock);
        }
        _count--;
    }

private:
    std::mutex _mtx;
    std::condition_variable _cv;
    int _count;
};

#define DEC_UNIQUE(cls)                   \
    cls(const cls &) = delete;            \
    cls(cls &&) = delete;                 \
    cls &operator=(const cls &) = delete; \
    cls &operator=(cls &&) = delete;

class RWLockSemaphore
{
public:
    RWLockSemaphore(bool dbg = false) : _w_mtx(1), _c_mtx(1), _read_cnt(0) {}
    DEC_UNIQUE(RWLockSemaphore)

    void lock(bool is_read)
    {
        if (is_read)
        {
            _c_mtx.wait();
            if (_read_cnt == 0)
                _w_mtx.wait();
            ++_read_cnt;
            _c_mtx.signal();
        }
        else
        {
            _w_mtx.wait();
        }
    }

    void unlock(bool is_read)
    {
        if (is_read)
        {
            _c_mtx.wait();
            --_read_cnt;
            if (_read_cnt == 0)
                _w_mtx.signal();
            _c_mtx.signal();
        }
        else
        {
            _w_mtx.signal();
        }
    }

private:
    Semaphore _w_mtx, _c_mtx;
    int _read_cnt;
};

class RWLockCond
{
public:
    RWLockCond(bool debug = false) : _dbg(debug), _indent(0), _AR(0), _AW(0), _WR(0), _WW(0) {}
    DEC_UNIQUE(RWLockCond)

    void lock(bool is_read)
    {
        std::unique_lock<std::mutex> lock(_mutex);
        if (_dbg)
            printf("aMutex\n");
        bool called = false, printed = false;
        auto print_wait = [&]() {
            if (called && !printed)
            {
                printf("Wait\n");
                printed = true;
            }
            called = true;
        };
        if (is_read)
        {
            _WR += 1;
            _read_cond.wait(lock, [&]() {
                if (_dbg)
                    print_wait();
                return (_AW + _WW) == 0;
            });
            _WR -= 1;
            _AR += 1;
        }
        else
        {
            _WW += 1;
            _write_cond.wait(lock, [&]() {
                if (_dbg)
                    print_wait();
                return (_AW + _AR) == 0;
            });
            _WW -= 1;
            _AW += 1;
        }
        if (_dbg)
            printf("rMutex\n");
    }

    void unlock(bool is_read)
    {
        std::unique_lock<std::mutex> lock(_mutex);
        if (_dbg)
            printf("aMutex\n");
        if (is_read)
        {
            --_AR;
        }
        else
        {
            --_AW;
        }
        if (_WW > 0)
        {
            _write_cond.notify_one();
        }
        else if (_WR > 0)
        {
            _read_cond.notify_all();
        }
        if (_dbg)
            printf("rMutex\n");
    }

private:
    bool _dbg;
    int _indent;
    int _AR, _AW, _WR, _WW;
    std::mutex _mutex;
    std::condition_variable _read_cond;
    std::condition_variable _write_cond;
};

#ifdef READ_FIRST
RWLockSemaphore rw_lock;
#else
RWLockCond rw_lock;
#endif

constexpr int WORK_SPAN = 4;
constexpr int SLEEP_SPAN = 5;
constexpr int N = 5;

struct arg_struct
{
    arg_struct(int _id, int _start, int _work, std::string _indent) : id(_id), start(_start), work(_work), indent(_indent) {}
    arg_struct(int _id) : id(_id), start(0), work(0), indent(0) {}
    int id;
    int start;
    int work;
    std::string indent;
};

int data = 0;

void reader(arg_struct *arg)
{
    sleep(arg->start);
    const char *indent = arg->indent.c_str();
    printf("%sStart\n", indent);
    rw_lock.lock(true);

    printf("%ssRead:%d\n", indent, data);
    sleep(arg->work);
    printf("%seRead:%d\n", indent, data);

    rw_lock.unlock(true);
    printf("%sExit\n", indent);
    delete arg;
}

void writer(arg_struct *arg)
{
    sleep(arg->start);
    const char *indent = arg->indent.c_str();
    printf("%sStart\n", indent);

    rw_lock.lock(false);

    printf("%ssWrite:%d\n", indent, data);
    ++data;
    sleep(arg->work);
    printf("%seWrite:%d\n", indent, data);

    rw_lock.unlock(false);
    printf("%sExit\n", indent);
    delete arg;
}

enum op_type
{
    READER = 0,
    WRITER
};

int main()
{
    int st_time = 0;
    int inst[2 * N][3] = {
        {READER, st_time += 0, rand() % WORK_SPAN},
        {READER, st_time += 1, rand() % WORK_SPAN},
        {READER, st_time += 0, rand() % WORK_SPAN},
        {WRITER, st_time += 4, rand() % WORK_SPAN},
        {READER, st_time += 0, rand() % WORK_SPAN},
        {WRITER, st_time += 1, rand() % WORK_SPAN},
        {READER, st_time += 0, rand() % WORK_SPAN},
        {READER, st_time += 0, rand() % WORK_SPAN},
        {WRITER, st_time += 1, rand() % WORK_SPAN},
        {READER, st_time += 0, rand() % WORK_SPAN}};

    std::vector<std::thread> workers;
    int tmp_r = 0, tmp_w = 0;
    for (auto &item : inst)
    {
        if (item[0] == READER)
        {
            printf("R%d\t", tmp_r++);
        }
        else if (item[0] == WRITER)
        {
            printf("W%d\t", tmp_w++);
        }
    }
    std::cout << std::endl;
    int r_count = 0, w_count = 0;
    std::string indent = "";
    for (auto &item : inst)
    {
        workers.emplace_back(std::thread(item[0] == READER ? reader : writer, new arg_struct(r_count++, item[1], item[2], indent)));
        indent += "\t";
    }

    for (auto &item : workers)
    {
        item.join();
    }
    return 0;
}