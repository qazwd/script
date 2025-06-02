import time
import sys
import threading

class Time_record:
    """实时追踪程序运行时间的类，支持记录多个时间片段"""
    
    def __init__(self):
        self.start_time = None
        self.total_time = 0
        self.running = False
        self._display_thread = None
        self._last_display_length = 0
        self.time_segments = []  # 存储每次运行的时间片段
        self.final_stop = False  # 标记是否为最终停止
    
    def start(self):
        """开始追踪运行时间"""
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self._display_thread = threading.Thread(target=self._update_display, daemon=True)  # 后台线程
            self._display_thread.start()  # 启动实时显示线程
    
    def stop(self, final=False):
        """停止追踪运行时间
        final: 是否为最终停止（程序结束），若是则显示总时间
        """
        if self.running:
            elapsed = time.time() - self.start_time
            self.total_time += elapsed
            self.time_segments.append(elapsed)  # 记录本次运行时间
            self.running = False
            self._clear_last_line()
            
            # 只显示当前片段用时，并确保清除残留
            self._print_segment_time(elapsed)
            
            self.final_stop = final
            if final:
                self._print_total_time()  # 程序结束时显示总时间
                
            return self.total_time
        return self.total_time
    
    def reset(self):
        """重置运行时间，但保留历史记录"""
        if self.running:
            self.stop()  # 先停止当前计时，记录时间片段
        self.start_time = None
        self.total_time = 0
        self.running = False
    
    def get_all_runs_total(self):
        """返回所有运行阶段的总时间"""
        return sum(self.time_segments)
    
    def clear_history(self):
        """清空所有历史记录"""
        self.time_segments = []
    
    def print_last_segment(self):
        """打印最后一个时间片段的信息"""
        if not self.time_segments:
            print("没有记录的时间片段")
            return
        print(f"最近一次运行时间: {self._format_time(self.time_segments[-1])}")
    
    def print_all_segments(self):
        """打印所有时间片段的信息"""
        if not self.time_segments:
            print("没有记录的时间片段")
            return
        print("所有运行时间片段:")
        for i, segment in enumerate(self.time_segments, 1):
            print(f"  片段 {i}: {self._format_time(segment)}")
    
    def record_reset(self):
        """显示所有阶段总时间，然后清除历史记录"""
        total_time = self.get_all_runs_total()
        self.print_all_segments()  # 先显示所有时间片段
        print(f"\n所有阶段总时间: {self._format_time(total_time)}")
        self.clear_history()
        print("已清除所有历史记录")
    
    def _format_time(self, seconds):
        """将秒数转换为时分秒的格式"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"
    
    def _update_display(self):
        """在终端最后一行实时更新运行时间"""
        while self.running:
            elapsed = time.time() - self.start_time  # 实时计算
            current_total = self.total_time + elapsed  # 计算当前总时间
            self._clear_last_line()  # 清除上一次的显示
            display_text = f"片段用时: {self._format_time(elapsed)} | 总用时: {self._format_time(current_total)}"
            self._last_display_length = len(display_text)  # 记录当前显示长度
            sys.stdout.write(f"{display_text}\r")  # 实时显示
            sys.stdout.flush()  # 确保立即显示
            time.sleep(0.1)
    
    def _clear_last_line(self):
        """清除终端最后一行"""
        sys.stdout.write('\r' + ' ' * self._last_display_length + '\r')  # 清除上一次的显示
        sys.stdout.flush()  # 确保立即显示
    
    def _print_segment_time(self, seconds):
        """打印片段用时并确保清除残留"""
        self._clear_last_line()
        text = f"片段用时: {self._format_time(seconds)}\n"
        sys.stdout.write(text)
        sys.stdout.flush()
    
    def _print_total_time(self):
        """打印总运行时间"""
        self._clear_last_line()
        text = f"程序总用时: {self._format_time(self.total_time)}\n"
        sys.stdout.write(text)
        sys.stdout.flush()

# 示例使用
if __name__ == "__main__":
    tracker = Time_record()
    
    try:
        # 第一次运行：2秒
        print("第一次运行开始...")
        tracker.start()
        time.sleep(2)
        tracker.stop()  # 普通停止，只显示片段用时
        
        # 重置后第二次运行：3秒
        print("\n第二次运行开始...")
        tracker.reset()
        tracker.start()
        time.sleep(3)
        tracker.stop(final=True)  # 最终停止，显示总时间
        
    except KeyboardInterrupt:
        tracker.stop(final=True)  # 中断时也显示总时间
        print("\n程序被用户中断")

    finally:
        # 显示所有阶段总时间并清除历史记录
        tracker.record_reset()
