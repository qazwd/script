//
/*
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// 平台特定的头文件和函数
#if defined(_WIN32)
    #include <windows.h>
    #include <conio.h>
    #define sleep(seconds) Sleep((seconds) * 1000)
    #define usleep(microseconds) Sleep((microseconds) / 1000)
#else
    #include <unistd.h>
    #include <sys/ioctl.h>
    #include <pthread.h>
    #include <time.h>
#endif

// 时间追踪器结构体
typedef struct {
    double start_time;
    double segment_time;
    double time_segment;
    double total_time;
    int running;
    int start_segment_time;
    double* time_segments;
    int time_segments_count;
    
    #if defined(_WIN32)
        HANDLE display_thread;
        HANDLE mutex;
    #else
        pthread_t display_thread;
        pthread_mutex_t mutex;
    #endif
} TimeTracer;

// 清除配置结构体
typedef struct {
    int time_segments;
    int total_time;
    int start_time;
    int segment_time;
    int time_segment;
    int running;
    int start_segment_time;
} ClearConfig;

// 函数原型
void TimeTracer_init(TimeTracer* tracer);
void TimeTracer_start(TimeTracer* tracer);
void TimeTracer_sets(TimeTracer* tracer);
void TimeTracer_stop(TimeTracer* tracer, int record);
void TimeTracer_record(TimeTracer* tracer);
void TimeTracer_clear_history(TimeTracer* tracer, ClearConfig config);
char* TimeTracer_format_time(double seconds);
int get_terminal_columns();

// 跨平台时间函数
double get_current_time() {
    #if defined(_WIN32)
        static LARGE_INTEGER frequency;
        static int initialized = 0;
        if (!initialized) {
            QueryPerformanceFrequency(&frequency);
            initialized = 1;
        }
        
        LARGE_INTEGER counter;
        QueryPerformanceCounter(&counter);
        return (double)counter.QuadPart / frequency.QuadPart;
    #else
        struct timespec ts;
        clock_gettime(CLOCK_MONOTONIC, &ts);
        return ts.tv_sec + ts.tv_nsec / 1e9;
    #endif
}

// 跨平台线程函数
#if defined(_WIN32)
    DWORD WINAPI TimeTracer_real_time_display(LPVOID arg) {
#else
    void* TimeTracer_real_time_display(void* arg) {
#endif
    TimeTracer* tracer = (TimeTracer*)arg;
    
    while (1) {
        // 加锁
        #if defined(_WIN32)
            WaitForSingleObject(tracer->mutex, INFINITE);
        #else
            pthread_mutex_lock(&tracer->mutex);
        #endif
        
        if (!tracer->running) {
            // 解锁
            #if defined(_WIN32)
                ReleaseMutex(tracer->mutex);
            #else
                pthread_mutex_unlock(&tracer->mutex);
            #endif
            break;
        }
        
        double now = get_current_time();
        double real_total = now - tracer->start_time;
        
        if (tracer->start_segment_time) {
            double real_segment = now - tracer->segment_time;
            char* segment_time = TimeTracer_format_time(real_segment);
            char* total_time = TimeTracer_format_time(real_total);
            
            char text_display[256];
            snprintf(text_display, sizeof(text_display), "该过程用时：%s | 总用时：%s ", segment_time, total_time);
            
            free(segment_time);
            free(total_time);
            
            // 右对齐显示
            int text_length = strlen(text_display);// - 2;
            printf("\r");
            for (int i = 0; i < get_terminal_columns() - text_length; i++) {
                printf(" ");
            }
            printf("%s", text_display);
            fflush(stdout);
        } else {
            char* total_time = TimeTracer_format_time(real_total);
            char text_display[256];
            snprintf(text_display, sizeof(text_display), "总用时：%s", total_time);
            
            free(total_time);
            
            // 右对齐显示
            int text_length = strlen(text_display);
            printf("\r");
            for (int i = 0; i < get_terminal_columns() - text_length; i++) {
                printf(" ");
            }
            printf("%s", text_display);
            fflush(stdout);
        }
        
        // 解锁
        #if defined(_WIN32)
            ReleaseMutex(tracer->mutex);
        #else
            pthread_mutex_unlock(&tracer->mutex);
        #endif
        
        usleep(100000); // 0.1秒
    }
    
    #if defined(_WIN32)
        return 0;
    #else
        return NULL;
    #endif
}

// 初始化时间追踪器
void TimeTracer_init(TimeTracer* tracer) {
    tracer->start_time = 0.0;
    tracer->segment_time = 0.0;
    tracer->time_segment = 0.0;
    tracer->total_time = 0.0;
    tracer->running = 0;
    tracer->start_segment_time = 0;
    tracer->time_segments = NULL;
    tracer->time_segments_count = 0;
    
    #if defined(_WIN32)
        tracer->mutex = CreateMutex(NULL, FALSE, NULL);
    #else
        pthread_mutex_init(&tracer->mutex, NULL);
    #endif
}

// 开始计时
void TimeTracer_start(TimeTracer* tracer) {
    if (!tracer->running) {
        tracer->start_time = get_current_time();
        tracer->running = 1;
        
        #if defined(_WIN32)
            tracer->display_thread = CreateThread(NULL, 0, TimeTracer_real_time_display, tracer, 0, NULL);
        #else
            pthread_create(&tracer->display_thread, NULL, TimeTracer_real_time_display, tracer);
        #endif
    } else {
        printf("计时已经开始！\n");
    }
}

// 片段计时
void TimeTracer_sets(TimeTracer* tracer) {
    // 加锁
    #if defined(_WIN32)
        WaitForSingleObject(tracer->mutex, INFINITE);
    #else
        pthread_mutex_lock(&tracer->mutex);
    #endif
    
    if (tracer->start_segment_time) {
        tracer->start_segment_time = 0;
        double now = get_current_time();
        tracer->time_segment = now - tracer->segment_time;
        
        // 添加到时间片段数组
        tracer->time_segments_count++;
        tracer->time_segments = realloc(tracer->time_segments, tracer->time_segments_count * sizeof(double));
        tracer->time_segments[tracer->time_segments_count - 1] = tracer->time_segment;
        
        char* formatted_time = TimeTracer_format_time(tracer->time_segment);
        printf("\n该过程用时：%s\n", formatted_time);
        free(formatted_time);
        
        tracer->segment_time = 0.0;
    } else {
        tracer->start_segment_time = 1;
        tracer->segment_time = get_current_time();
        
        #if defined(_WIN32)
            tracer->display_thread = CreateThread(NULL, 0, TimeTracer_real_time_display, tracer, 0, NULL);
        #else
            pthread_create(&tracer->display_thread, NULL, TimeTracer_real_time_display, tracer);
        #endif
    }
    
    // 解锁
    #if defined(_WIN32)
        ReleaseMutex(tracer->mutex);
    #else
        pthread_mutex_unlock(&tracer->mutex);
    #endif
}

// 停止计时
void TimeTracer_stop(TimeTracer* tracer, int record) {
    // 加锁
    #if defined(_WIN32)
        WaitForSingleObject(tracer->mutex, INFINITE);
    #else
        pthread_mutex_lock(&tracer->mutex);
    #endif
    
    if (tracer->running) {
        double now = get_current_time();
        double total = now - tracer->start_time;
        tracer->running = 0;
        
        // 解锁
        #if defined(_WIN32)
            ReleaseMutex(tracer->mutex);
        #else
            pthread_mutex_unlock(&tracer->mutex);
        #endif
        
        if (record && tracer->time_segments_count > 0) {
            tracer->total_time += total;
            TimeTracer_record(tracer);
        }
        
        char* formatted_time = TimeTracer_format_time(total);
        printf("总用时：%s\n", formatted_time);
        free(formatted_time);
        
        // 默认清除所有
        ClearConfig config = {1, 1, 1, 1, 1, 1, 1};
        TimeTracer_clear_history(tracer, config);
    } else {
        printf("计时还未开始！\n");
        
        // 解锁
        #if defined(_WIN32)
            ReleaseMutex(tracer->mutex);
        #else
            pthread_mutex_unlock(&tracer->mutex);
        #endif
    }
}

// 格式化时间
char* TimeTracer_format_time(double seconds) {
    int hours = (int)seconds / 3600;
    int minutes = ((int)seconds % 3600) / 60;
    double secs = fmod(seconds, 60.0);
    
    char* buffer = malloc(32);
    snprintf(buffer, 32, "%02d:%02d:%05.2f", hours, minutes, secs);
    return buffer;
}

// 获取终端列数
int get_terminal_columns() {
    #if defined(_WIN32)
        CONSOLE_SCREEN_BUFFER_INFO csbi;
        GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
        return csbi.srWindow.Right - csbi.srWindow.Left + 1;
    #else
        struct winsize w;
        ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);
        return w.ws_col;
    #endif
}

// 记录运行时间
void TimeTracer_record(TimeTracer* tracer) {
    printf("            ***------------ 运行记录 ------------***\n");
    printf("\n              所有过程运行时间:\n");
    
    double sum = 0.0;
    for (int i = 0; i < tracer->time_segments_count; i++) {
        char* formatted_time = TimeTracer_format_time(tracer->time_segments[i]);
        printf("                  过程 %d 用时: %s\n", i + 1, formatted_time);
        free(formatted_time);
        sum += tracer->time_segments[i];
    }
    
    char* formatted_sum = TimeTracer_format_time(sum);
    printf("                所有过程总用时: %s\n\n", formatted_sum);
    free(formatted_sum);
    printf("            ***----------------------------------***\n");
}

// 清除历史记录
void TimeTracer_clear_history(TimeTracer* tracer, ClearConfig config) {
    // 加锁
    #if defined(_WIN32)
        WaitForSingleObject(tracer->mutex, INFINITE);
    #else
        pthread_mutex_lock(&tracer->mutex);
    #endif
    
    if (config.time_segments) {
        free(tracer->time_segments);
        tracer->time_segments = NULL;
        tracer->time_segments_count = 0;
    }
    if (config.total_time) {
        tracer->total_time = 0.0;
    }
    if (config.start_time) {
        tracer->start_time = 0.0;
    }
    if (config.segment_time) {
        tracer->segment_time = 0.0;
    }
    if (config.time_segment) {
        tracer->time_segment = 0.0;
    }
    if (config.running) {
        tracer->running = 0;
    }
    if (config.start_segment_time) {
        tracer->start_segment_time = 0;
    }
    
    // 解锁
    #if defined(_WIN32)
        ReleaseMutex(tracer->mutex);
    #else
        pthread_mutex_unlock(&tracer->mutex);
    #endif
}


// 测试代码
int main() {
    TimeTracer tracer;
    TimeTracer_init(&tracer);
    
    printf("\n开始计时\n");
    TimeTracer_start(&tracer);
    sleep(1);
    
    printf("\n过程1开始\n");
    TimeTracer_sets(&tracer);
    sleep(1);
    TimeTracer_sets(&tracer);
    printf("\n过程1结束\n");
    
    sleep(1);
    printf("\n过程2开始\n");
    TimeTracer_sets(&tracer);
    sleep(1);
    TimeTracer_sets(&tracer);
    printf("\n过程2结束\n");
    
    sleep(1);
    TimeTracer_stop(&tracer, 1);
    
    // 清理资源
    free(tracer.time_segments);
    
    #if defined(_WIN32)
        CloseHandle(tracer.mutex);
    #else
        pthread_mutex_destroy(&tracer.mutex);
    #endif
    
    return 0;
}
//*/