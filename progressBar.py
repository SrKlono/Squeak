import time
import threading

class ProgressBar:
    def __init__(self, window, duration=100, callback=None):
        self.window = window
        self.duration = duration
        self.paused = False
        self.callback = callback
        self.reset()

    def reset(self):
        self.startTime = time.time()
        self.timePassed = 0

    def pause(self):
        self.paused = True
        self.pauseTime = time.time()
        
    def resume(self):
        self.paused = False
        if hasattr(self, 'pauseTime'):
            self.startTime += time.time() - self.pauseTime
            del self.pauseTime

    def updateProgress(self):
        while self.timePassed < self.duration/1000:
            if not self.paused:
                self.timePassed = time.time() - self.startTime
            time.sleep(0.1)
            self.displayProgress()

        # Execute callback if there is any
        if self.callback:
            self.callback()

    def displayProgress(self):
        progress = min(1.0, self.timePassed / (self.duration / 1000))
        barWidth = 50
        filledWidth = int(barWidth * progress)
        emptyWidth = barWidth - filledWidth
        barText = '┝' + '━' * filledWidth + '─' * emptyWidth + '┤'
        dims = self.window.getmaxyx()
        self.window.addstr(
            int(int(dims[0])-5),
            int(int(dims[1]/2)) - int((len(barText)+12)/2), 
            f'{formatDuration(self.timePassed * 1000)} ' +
            "{}".format(barText, progress * 100) + 
            f' {formatDuration(self.duration)}'
        )
        
        self.window.refresh()

    def start(self):
        self.reset()
        threading.Thread(target=self.updateProgress, daemon=True).start()

def formatDuration(ms):
    totalSec = ms / 1000
    totalMin = totalSec / 60
    remainSec = totalSec % 60
    return "%0d:%02d" % (totalMin, remainSec)