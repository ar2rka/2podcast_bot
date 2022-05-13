from grabber.Grabber import Grabber
from pytube import YouTube

FILE_PATH = 'media/'


class YTGrabber(Grabber):
    def connect(self):
        self.conn = YouTube(self.source)

    def download(self, file_type='audio', quality=None):
        if file_type == 'audio':
            stream = self.conn.streams.filter(only_audio=True).first()
        else:
            stream = self.conn.streams.filter()
        # if quality:
        #     closest_quality = 0
        #     for i in self.conn.streams.filter(only_audio=True):
        print(stream)
        # logger.debug(f"video contains: {stream})
        title = self.conn.title.replace(' ', '_')
        filename = ''.join(filter(lambda s: (s.isalpha() or s == '_' or s.s.isdigit()),
                                  self.conn.title.replace(' ', '_')))
        # filename = self.conn.title.replace(' ', '_')
        stream.download(output_path=FILE_PATH, filename=filename)
        return filename, title
