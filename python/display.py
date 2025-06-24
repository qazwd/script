import time
import shutil
import threading

class TimeTracer:
    '''实时显示程序运行时间'''

    def __init__(self) -> None:
        self.start_time = 0             # 开始时间
        self.segment_time = 0           # 片段时间
        self.time_segment = 0           # 记录每次运行时间
        self.total_time = 0             # 总时间

        self.running = False             # 是否正在运行
        self.record = False               # 记录函数
        self.start_segment_time = False  # 是否开始片段计时
        self.time_segments = []          # 记录每次运行时间的列表S

    def start(self):
        '''开始计时'''
        if not self.running:     # 如果不在运行中
            self.start_time = time.time()      # 记录开始时间
            self.running = True                # 标记为正在运行
            self._display_thread = threading.Thread(target=self._real_time_display, daemon=True)  # 后台线程
            self._display_thread.start()       # 启动实时显示线程
        else:                    # 如果已经在运行中
            raise ValueError("计时已经开始！")  # 抛出异常

    def sets(self, record=False):
        '''片段计时'''
        if self.start_segment_time:      # 如果已经开始片段计时
            self.start_segment_time = False                      # 标记为停止片段计时
            self.time_segment = time.time() - self.segment_time  # 计算本次运行时间
            self.time_segments.append(self.time_segment)         # 记录本次运行时间
            text_display = f"该过程用时：{self._set_format_time(self.time_segment)} "
            text_length = len(text_display + 5 * ' ')                    # 计算文本长度
            self._right_print_time_and_clear(text_display, text_length)  # 右对齐显示文本
            self.segment_time = 0                                # 重置片段时间
            if record:
                self.records()
                self.clear_history()
        else:                            # 如果还没有开始片段计时
            self.start_segment_time = True                       # 标记为开始片段计时
            self.segment_time = time.time()                      # 记录片段开始时间
            self._display_thread = threading.Thread(target=self._real_time_display, daemon=True)  # 后台线程
            self._display_thread.start()                        # 启动实时显示线程

    def stop(self, record=True):
        '''停止计时'''
        if self.running:
            self.running = False                        # 标记为停止
            total_time = time.time() - self.start_time  # 计算总时间
            if record and self.time_segments:     # 如果需要显示记录
                self.total_time += total_time           # 累加总时间
                self.records()                           # 显示记录
            print(f"总用时：{self._set_format_time(total_time)}")         # 显示总时间
            self.clear_history()                        # 清除历史记录
        elif not self.running:       # 如果时间并没有开始
            # 抛出异常
            raise ValueError("计时还未开始！")

    def _real_time_display(self):
        '''实时显示程序运行时间'''
        if self.running:
            while self.start_segment_time:               # 当开始片段计时时
                real_segment_time = time.time() - self.segment_time                # 计算片段时间
                real_total_time = time.time() - self.start_time                    # 计算总时间
                text_display = f"该过程用时：{self._set_format_time(real_segment_time)} | 总用时：{self._set_format_time(real_total_time)} "
                text_length = len(text_display + 10 * ' ')                         # 计算文本长度
                self._right_print_time_and_clear(text_display, text_length)        # 右对齐显示文本
                time.sleep(0.1)

            while not self.start_segment_time and self.running:            # 当正在运行时, 且没有开始片段计时时
                real_total_time = time.time() - self.start_time                    # 计算总时间
                real_total_time = self._set_format_time(real_total_time)           # 格式化总时间
                text_display = f"总用时：{real_total_time}"                         # 构造显示文本
                text_length = len(text_display + 4 * ' ')                          # 计算文本长度
                self._right_print_time_and_clear(text_display, text_length)        # 右对齐显示文本
                time.sleep(0.1)
        else:
            raise ValueError("无法实时显示")

    def _set_format_time(self, seconds):
        '''格式化时间'''
        hours, remainder = divmod(seconds, 3600)  # 计算小时和剩余时间
        minutes, seconds = divmod(remainder, 60)  # 计算分钟和剩余秒数
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"

    def _right_print_time_and_clear(self, text_display, text_length):
        '''右对齐显示时间'''
        columns = shutil.get_terminal_size().columns    # 获取终端宽度
        text_right = text_display[:columns - 4] + "..." if len(text_display) > columns else text_display
        spaces = max(0, columns - text_length)                       # 计算需要填充的空格数
        print('\033[2K\r' + ' ' * columns + '\033[2K\r' + ' ' * spaces + text_right, end='', flush=True)

    def records(self):
        '''显示运行片段'''
        print(f"{13*' '}***------------ 运行记录 ------------***")
        print(f"\n {16*' '} 所有过程运行时间:")                                                  # 显示所有运行时间片段
        for i, segment in enumerate(self.time_segments, 1):                                    # 遍历记录列表
            print(f" {20*' '} 过程 {i} 用时: {self._set_format_time(segment)}")                     # 显示每个运行时间片段
        print(f" {18*' '} 所有过程总用时: {self._set_format_time(sum(self.time_segments))}\n")   # 显示所有运行时间片段的总时间
        print(f"{13*' '}***----------------------------------***")

    def clear_history(self, **kwargs):
        '''清除历史记录'''
        defaults = {
            'time_segments': True,
            'total_time': True,
            'start_time': True,
            'segment_time': True,
            'time_segment': True,
            'running': True,
            'start_segment_time': True
        }
        for attr, value in {**defaults, **kwargs}.items():
            if value:
                setattr(self, attr, [] if attr == 'time_segments' else False if attr in ('running', 'start_segment_time') else 0)

    def __enter__(self): 
        """进入上下文管理器时启动计时"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开上下文管理器时停止计时，遇到异常也会执行"""
        if self.running:
            self.stop()
        # 让异常继续传播
        return False

    def __del__(self):
        """析构函数，确保在对象销毁时停止计时"""
        if self.running:
            self.stop()


# 运行动画
class RunningAnimation:
    '''
    运行动画类
    用于在控制台实时显示运行中的动画效果，如加载、进度条等。
    '''

    def __init__(self, run_chars, interval=0.1):
        self.run_chars = run_chars    # 动画字符
        self.interval = interval                  # 动画间隔
        self.is_running = False                   # 是否正在运行
        self.thread = None                        # 线程
        self.current_line = shutil.get_terminal_size().lines  # 记录当前动画所在行

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_animation, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)  # 等待线程结束，最多等待1秒
        # 清除最后显示的动画字符
        columns = shutil.get_terminal_size().columns
        print(f"\033[{self.current_line};{columns}H ", end='', flush=True)

    def _run_animation(self):
        while self.is_running:
            for char in self.run_chars:
                columns = shutil.get_terminal_size().columns
                lines = shutil.get_terminal_size().lines
                # 确保 current_line 不超过终端行数
                if self.current_line > lines:
                    self.current_line = lines
                # 移动到终端底部右侧位置
                print(f"\033[{self.current_line};{columns}H{char}", end='', flush=True)
                time.sleep(self.interval)

    def __enter__(self):
        """进入上下文管理器时启动动画"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开上下文管理器时停止动画"""
        self.stop()
        if exc_type:
            return False
        return self
        
    def __del__(self): 
        """析构函数，确保在对象销毁时及时清除输出"""
        self.stop()


# 测试代码
#
'''
if __name__ == '__main__':
    # 方法一：
    time_tracer = TimeTracer()
    print("\n开始计时")
    time_tracer.start()
    time.sleep(2)
    print("\n过程1开始")
    time_tracer.sets()
    time.sleep(2)
    time_tracer.sets()
    print("\n过程1结束")
    time.sleep(2)
    print("\n过程2开始")
    time_tracer.sets()
    time.sleep(2)
    time_tracer.sets()
    print("\n过程2结束")
    time.sleep(2)
    time_tracer.stop()
    # 方法二：
    with TimeTracer() as time_tracer:
        time.sleep(2)
        print("\n过程1开始")
        time_tracer.sets()
        time.sleep(2)
        time_tracer.sets()
        print("\n过程1结束")
        time.sleep(2)
        time_tracer.sets()
        time.sleep(2)
        time_tracer.stop()

print('\033[2K\r' + ' ' * columns + '\033[2K\r' + ' ' * spaces + text_right, end='', flush=True)
#'''
# 测试动画
#'''
if __name__ == '__main__':
    # 方法一：
    run_chars = ['|', '/', '-', '\\']
    with RunningAnimation(run_chars, interval=0.2) as anim:
        time.sleep(5)  # 模拟长时间运行的任务
    print("\n动画结束")
    # 方法二：
    run_chars = ['|', '/', '-', '\\']
    anim = RunningAnimation(run_chars, interval=0.2)
    anim.start()  # 启动动画
    try:
        time.sleep(5)  # 模拟长时间运行的任务
    finally:
        anim.stop()  # 确保动画停止
    print("\n动画结束")
#'''
