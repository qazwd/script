/*
#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <iomanip>
#include <mutex>
#include <sstream>
#include <windows.h>

class TimeTracer {
public:
    // 清除配置结构体
    struct ClearConfig {
        bool time_segments = true;
        bool total_time = true;
        bool start_time = true;
        bool segment_time = true;
        bool time_segment = true;
        bool running = true;
        bool start_segment_time = true;
        
        ClearConfig& set_time_segments(bool value) { time_segments = value; return *this; }
        ClearConfig& set_total_time(bool value) { total_time = value; return *this; }
        ClearConfig& set_start_time(bool value) { start_time = value; return *this; }
        ClearConfig& set_segment_time(bool value) { segment_time = value; return *this; }
        ClearConfig& set_time_segment(bool value) { time_segment = value; return *this; }
        ClearConfig& set_running(bool value) { running = value; return *this; }
        ClearConfig& set_start_segment_time(bool value) { start_segment_time = value; return *this; }
    };

    TimeTracer() 
        : start_time(std::chrono::steady_clock::now()),
          segment_time(std::chrono::steady_clock::now()),
          time_segment(0),
          total_time(0),
          running(false),
          start_segment_time(false) {}

    void start() {
        if (!running) {
            start_time = std::chrono::steady_clock::now();
            running = true;
            display_thread = std::thread(&TimeTracer::_real_time_display, this);
            display_thread.detach();
        } else {
            throw std::runtime_error("计时已经开始！");
        }
    }

    void sets() {
        std::lock_guard<std::mutex> lock(mtx);
        if (start_segment_time) {
            start_segment_time = false;
            auto now = std::chrono::steady_clock::now();
            time_segment = std::chrono::duration<double>(now - segment_time).count();
            time_segments.push_back(time_segment);
            
            std::ostringstream oss;
            oss << "该过程用时：" << _format_time(time_segment) << " ";
            std::string text_display = oss.str();
            
            int text_length = text_display.length() + 6;
            _right_print_time_and_clear(text_display, text_length);
        } else {
            start_segment_time = true;
            segment_time = std::chrono::steady_clock::now();
            display_thread = std::thread(&TimeTracer::_real_time_display, this);
            display_thread.detach();
        }
    }

    void stop(bool record = true) {
        std::unique_lock<std::mutex> lock(mtx);
        if (running) {
            auto now = std::chrono::steady_clock::now();
            double total = std::chrono::duration<double>(now - start_time).count();
            running = false;
            lock.unlock();
            
            if (record && !time_segments.empty()) {
                total_time += total;
                this->record();
            }
            
            std::cout << "总用时：" << _format_time(total) << std::endl;
            clear_history(); // 使用默认配置清除
        } else {
            throw std::runtime_error("计时还未开始！");
        }
    }

    // 清除历史记录（使用配置）
    void clear_history(const ClearConfig& config = ClearConfig()) {
        std::lock_guard<std::mutex> lock(mtx);
        
        if (config.time_segments) {
            time_segments.clear();
        }
        if (config.total_time) {
            total_time = 0.0;
        }
        if (config.start_time) {
            start_time = std::chrono::steady_clock::time_point();
        }
        if (config.segment_time) {
            segment_time = std::chrono::steady_clock::time_point();
        }
        if (config.time_segment) {
            time_segment = 0.0;
        }
        if (config.running) {
            running = false;
        }
        if (config.start_segment_time) {
            start_segment_time = false;
        }
    }

private:
    std::chrono::steady_clock::time_point start_time;
    std::chrono::steady_clock::time_point segment_time;
    double time_segment;
    double total_time;
    bool running;
    bool start_segment_time;
    std::vector<double> time_segments;
    std::thread display_thread;
    std::mutex mtx;

    std::string _format_time(double seconds) {
        int hours = static_cast<int>(seconds) / 3600;
        int minutes = (static_cast<int>(seconds) % 3600) / 60;
        double secs = seconds - hours * 3600 - minutes * 60;
        
        std::ostringstream oss;
        oss << std::setfill('0') << std::setw(2) << hours << ":"
            << std::setfill('0') << std::setw(2) << minutes << ":"
            << std::fixed << std::setprecision(2) << secs;
        return oss.str();
    }

    void _right_print_time_and_clear(const std::string& text_display, int text_length) {
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        CONSOLE_SCREEN_BUFFER_INFO csbi;
        GetConsoleScreenBufferInfo(hConsole, &csbi);
        int columns = csbi.srWindow.Right - csbi.srWindow.Left + 1;
        
        std::string text_right;
        if (text_display.length() > static_cast<size_t>(columns - 4)) {
            text_right = text_display.substr(0, columns - 7) + "...";
        } else {
            text_right = text_display;
        }
        
        int spaces = std::max(0, columns - text_length);
        std::cout << "\r" << std::string(spaces, ' ') << text_right << std::flush;
    }

    void _real_time_display() {
        while (true) {
            {
                std::lock_guard<std::mutex> lock(mtx);
                if (!running) break;
                
                auto now = std::chrono::steady_clock::now();
                double real_total = std::chrono::duration<double>(now - start_time).count();
                
                if (start_segment_time) {
                    double real_segment = std::chrono::duration<double>(now - segment_time).count();
                    std::ostringstream oss;
                    oss << "该过程用时：" << _format_time(real_segment) 
                        << " | 总用时：" << _format_time(real_total) << " ";
                    std::string text_display = oss.str();
                    int text_length = text_display.length() + 10;
                    _right_print_time_and_clear(text_display, text_length);
                } else {
                    std::ostringstream oss;
                    oss << "总用时：" << _format_time(real_total);
                    std::string text_display = oss.str();
                    int text_length = text_display.length() + 4;
                    _right_print_time_and_clear(text_display, text_length);
                }
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }

    void record() {
        std::cout << std::string(13, ' ') << "***------------ 运行记录 ------------***" << std::endl;
        std::cout << "\n" << std::string(16, ' ') << " 所有过程运行时间:" << std::endl;
        
        for (size_t i = 0; i < time_segments.size(); ++i) {
            std::cout << std::string(20, ' ') << " 过程 " << i+1 << " 用时: " 
                      << _format_time(time_segments[i]) << std::endl;
        }
        
        double sum = 0;
        for (double seg : time_segments) sum += seg;
        
        std::cout << std::string(18, ' ') << " 所有过程总用时: " 
                  << _format_time(sum) << "\n" << std::endl;
        std::cout << std::string(12, ' ') << "***----------------------------------***" << std::endl;
    }
};
/*
// 测试代码
int main() {
    TimeTracer tracer;
    
    try {
        std::cout << "\n开始计时" << std::endl;
        tracer.start();
        std::this_thread::sleep_for(std::chrono::seconds(1));
        
        std::cout << "\n过程1开始" << std::endl;
        tracer.sets();
        std::this_thread::sleep_for(std::chrono::seconds(1));
        tracer.sets();
        std::cout << "\n过程1结束" << std::endl;
        
        std::this_thread::sleep_for(std::chrono::seconds(1));
        std::cout << "\n过程2开始" << std::endl;
        tracer.sets();
        std::this_thread::sleep_for(std::chrono::seconds(1));
        tracer.sets();
        std::cout << "\n过程2结束" << std::endl;
        
        std::this_thread::sleep_for(std::chrono::seconds(1));
        tracer.stop();
        tracer.record();

        // 部分清除示例
        tracer.clear_history(TimeTracer::ClearConfig()
            .set_time_segments(true)   // 清除时间片段
            .set_time_segment(true)     // 清除当前片段
            .set_running(false)         // 保持运行状态不变
            .set_start_segment_time(false)); // 保持片段计时状态
    } catch (const std::exception& e) {
        std::cerr << "错误: " << e.what() << std::endl;
    }
    
    return 0;
}*/