import io
from typing import BinaryIO, Union

from . import exceptions, image_utils, utils


class ThecampyImage:
    metadata: image_utils.ImageMetadata
    saved_file_name: str
    file_path: str
    path: str
    ct: str
    fp: BinaryIO
    is_uploaded: bool

    def __init__(self, image_file: Union[str, bytes, BinaryIO], image_size=0):
        """
        :param image_file: 파일 경로, bytes, file like object, ThecampyImage 타입을 지원합니다.
        :param image_size: (optional) image_file 이 file like object 인 경우 image_size 를 지정합니다.
        """
        self.is_uploaded = False
        self._local_file_path = ''
        try:
            if isinstance(image_file, str):
                self._local_file_path = image_file
                self.metadata = image_utils.get_image_metadata(image_file)
            elif isinstance(image_file, bytes):
                image_size = len(image_file)
                with io.BytesIO(image_file) as buffer:
                    self.metadata = image_utils.get_image_metadata_from_bytesio(buffer, image_size)
                self.fp = io.BytesIO(image_file)
            elif isinstance(image_file, BinaryIO):
                if not image_size:
                    image_bytes = image_file.read()
                    image_size = len(image_bytes)
                self.metadata = image_utils.get_image_metadata_from_bytesio(image_file, image_size)
                image_file.seek(0)
                self.fp = image_file
            else:
                raise TypeError('`image_file` 는 file path str, image_file bytes, binary file like object 만 지원합니다.')
        except image_utils.UnknownImageFormat:
            raise exceptions.ThecampyValueError('지원되지 않는 이미지 포맷 이거나 잘못된 이미지 파일 입니다.') from None

        self.raise_invalid_image()

        now = utils.get_kr_now()
        date_str = now.strftime('%Y%m%d')
        name = f'{now.strftime("%Y%m%d%H%M%S%f")[:17]}_ge1'
        ext = self.metadata.type.lower()
        file_dir = f'/images/upload/{date_str}/1234/'
        path = f'{file_dir}{name}.{ext}'
        self.saved_file_name = name
        self.file_path = file_dir
        self.path = path
        self.ct = f'image_file/{ext}'

    def raise_invalid_image(self):
        allow_image_format = {'jpeg', 'png', 'bmp', 'jpg', 'gif'}
        if self.metadata.type.lower() not in allow_image_format:
            raise exceptions.ThecampyValueError('허용하지 않는 이미지 포맷입니다.')
        if 10_485_760 < self.metadata.file_size:
            raise exceptions.ThecampyValueError('10MB 를 초과하는 이미지를 업로드 할 수 없습니다.')

    def close(self):
        self.fp.close()

    def __enter__(self):
        if self.is_uploaded:
            raise exceptions.ThecampyReqError('이미 업로드 한 이미지 입니다.')
        if self._local_file_path:
            self.fp = open(self._local_file_path, 'rb')
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_uploaded = True
        self.close()
