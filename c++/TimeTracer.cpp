/*
#include <iostream>
#include <iomanip>
#include <thread>
#include <chrono>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <windows.h> // Windows API 头文件

class Time_tracer {
private:
    double start_time;
    double segment_time;
    double time_segment;
    double total_time;

    bool running;
    bool start_segment_time;
    std::vector<double> time_segments;

    // 格式化时间
    std::string _set_format_time(double seconds) {
        int hours = static_cast<int>(seconds / 3600);
        int minutes = static_cast<int>(fmod(seconds, 3600) / 60);  // 使用fmod函数替代%
        double secs = fmod(seconds, 60);  // 使用fmod函数替代%
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << hours << ":"
            << std::setfill('0') << std::setw(2) << minutes << ":"
            << std::fixed << std::setprecision(2) << secs;
        return oss.str();
    }

    // 获取控制台窗口宽度
    int get_console_width() {
        CONSOLE_SCREEN_BUFFER_INFO csbi;
        GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
        return csbi.srWindow.Right - csbi.srWindow.Left + 1;
    }

    // 右对齐显示时间
    void _right_print_time_and_clear(const std::string& text_display, int text_length) {
        int columns = get_console_width();
        std::string text_right = text_display;
        if (static_cast<int>(text_display.length()) > columns) {
            text_right = text_display.substr(0, columns - 4) + "...";
        }
        int spaces = std::max(0, columns - text_length);
        std::cout << "\r" << std::string(columns, ' ') << "\r"
                  << std::string(spaces, ' ') << text_right << std::flush;
    }

    // 实时显示程序运行时间
    void _real_time_display() {
        while (start_segment_time) {
            double real_segment_time = std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count() - segment_time;
            double real_total_time = std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count() - start_time;
            std::string text_display = "该过程用时：" + _set_format_time(real_segment_time) + " | 总用时：" + _set_format_time(real_total_time);
            int text_length = static_cast<int>(text_display.length());
            _right_print_time_and_clear(text_display, text_length);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }

        while (running && !start_segment_time) {
            double real_total_time = std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count() - start_time;
            std::string text_display = "总用时：" + _set_format_time(real_total_time);
            int text_length = static_cast<int>(text_display.length());
            _right_print_time_and_clear(text_display, text_length);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }

public:
    Time_tracer() : start_time(0), segment_time(0), time_segment(0), total_time(0),
                    running(false), start_segment_time(false) {}

    // 开始计时
    void start() {
        if (!running) {
            start_time = std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();
            running = true;
            std::thread display_thread(&Time_tracer::_real_time_display, this);
            display_thread.detach();
        } else {
            throw std::invalid_argument("计时已经开始！");
        }
    }

    // 片段计时
    void sets() {
        if (start_segment_time) {
            start_segment_time = false;
            time_segment = std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count() - segment_time;
            time_segments.push_back(time_segment);
            std::string text_display = "该过程用时：" + _set_format_time(time_segment);
            int text_length = static_cast<int>(text_display.length());
            _right_print_time_and_clear(text_display, text_length);
            segment_time = 0;
        } else {
            start_segment_time = true;
            segment_time = std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count();
            std::thread display_thread(&Time_tracer::_real_time_display, this);
            display_thread.detach();
        }
    }

    // 停止计时
    void stop(bool record = true) {
        if (running) {
            double total = std::chrono::duration<double>(std::chrono::steady_clock::now().time_since_epoch()).count() - start_time;
            running = false;
            if (record && !time_segments.empty()) {
                total_time += total;
                record_time();
            }
            std::cout << "\n总用时：" << _set_format_time(total) << std::endl;
            clear_history();
        } else {
            throw std::invalid_argument("计时还未开始！");
        }
    }

    // 记录运行时间
    void record_time() {
        std::cout << "             ***------------ 运行记录 ------------***" << std::endl;
        std::cout << "\n                  所有过程运行时间:" << std::endl;
        for (size_t i = 0; i < time_segments.size(); ++i) {
            std::cout << "                      过程 " << i + 1 << " 用时: " << _set_format_time(time_segments[i]) << std::endl;
        }
        double sum_time = 0;
        for (double segment : time_segments) {
            sum_time += segment;
        }
        std::cout << "                    所有过程总用时: " << _set_format_time(sum_time) << std::endl;
        std::cout << "             ***----------------------------------***" << std::endl;
    }

    // 清除历史记录
    void clear_history() {
        time_segments.clear();
        total_time = 0;
        start_time = 0;
        segment_time = 0;
        time_segment = 0;
        running = false;
        start_segment_time = false;
    }
};

int main() {
    Time_tracer time_tracer;
    std::cout << "\n开始计时" << std::endl;
    time_tracer.start();
    std::this_thread::sleep_for(std::chrono::seconds(2));
    std::cout << "\n过程1开始" << std::endl;
    time_tracer.sets();
    std::this_thread::sleep_for(std::chrono::seconds(2));
    time_tracer.sets();
    std::cout << "\n过程1结束" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2));
    std::cout << "\n过程2开始" << std::endl;
    time_tracer.sets();
    std::this_thread::sleep_for(std::chrono::seconds(2));
    time_tracer.sets();
    std::cout << "\n过程2结束" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2));
    time_tracer.stop();
    return 0;
}*/