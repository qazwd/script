import time
import shutil
import threading

class Time_tracer:
    '''实时显示程序运行时间'''

    def __init__(self) -> None:
        self.start_time = 0             # 开始时间
        self.segment_time = 0           # 片段时间
        self.time_segment = 0           # 记录每次运行时间
        self.total_time = 0             # 总时间

        self.running = False             # 是否正在运行
        self.start_segment_time = False  # 是否开始片段计时
        self.time_segments = []          # 记录每次运行时间的列表

    def start(self):
        '''开始计时'''
        if not self.running:     # 如果不在运行中
            self.start_time = time.time()      # 记录开始时间
            self.running = True                # 标记为正在运行
            self._display_thread = threading.Thread(target=self._real_time_display, daemon=True)  # 后台线程
            self._display_thread.start()       # 启动实时显示线程
        else:                    # 如果已经在运行中
            raise ValueError("计时已经开始！")  # 抛出异常

    def sets(self):
        '''片段计时'''
        if self.start_segment_time:      # 如果已经开始片段计时
            self.start_segment_time = False                      # 标记为停止片段计时
            self.time_segment = time.time() - self.segment_time  # 计算本次运行时间
            self.time_segments.append(self.time_segment)         # 记录本次运行时间
            text_display = f"该过程用时：{self._set_format_time(self.time_segment)} "
            text_length = len(text_display + 6 * ' ')                    # 计算文本长度
            self._right_print_time_and_clear(text_display, text_length)  # 右对齐显示文本
            self.segment_time = 0                                # 重置片段时间
        else:                            # 如果还没有开始片段计时
            self.start_segment_time = True                       # 标记为开始片段计时
            self.segment_time = time.time()                      # 记录片段开始时间
            self._display_thread = threading.Thread(target=self._real_time_display, daemon=True)  # 后台线程
            self._display_thread.start()                        # 启动实时显示线程

    def stop(self, record = True):
        '''停止计时'''
        if self.running:
            total_time = time.time() - self.start_time  # 计算总时间
            self.running = False                        # 标记为停止
            if record == True and self.time_segments:   # 如果需要记录
                self.total_time += total_time           # 累加总时间
                self.record()                           # 显示记录
            print(f"总用时：{self._set_format_time(total_time)}")         # 显示总时间
            self.clear_history()                        # 清除历史记录
        elif not self.running:       # 如果时间并没有开始
            # 抛出异常
            raise ValueError("计时还未开始！")
        
    def _start_display_thread(self):
        if not self._display_thread or not self._display_thread.is_alive():  # 检查线程是否存在且存活
            self._display_thread = threading.Thread(target=self._real_time_display, daemon=True)
            self._display_thread.start()

    def _real_time_display(self):
        '''实时显示程序运行时间'''
        while self.start_segment_time:               # 当开始片段计时时
            real_segment_time = time.time() - self.segment_time                # 计算片段时间
            real_total_time = time.time() - self.start_time                    # 计算总时间
            text_display = f"该过程用时：{self._set_format_time(real_segment_time)} | 总用时：{self._set_format_time(real_total_time)} "
            text_length = len(text_display + 10 * ' ')                    # 计算文本长度
            self._right_print_time_and_clear(text_display, text_length)        # 右对齐显示文本
            time.sleep(0.1)

        while not self.start_segment_time:            # 当正在运行时, 且没有开始片段计时时
            real_total_time = time.time() - self.start_time                    # 计算总时间
            real_total_time = self._set_format_time(real_total_time)           # 格式化总时间
            text_display = f"总用时：{real_total_time}"                         # 构造显示文本
            text_length = len(text_display + 4 * ' ')                          # 计算文本长度
            self._right_print_time_and_clear(text_display, text_length)        # 右对齐显示文本
            time.sleep(0.1)

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

    def record(self):
        '''记录运行时间'''
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

# 测试代码
'''
if __name__ == '__main__':
    time_tracer = Time_tracer()
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
'''
