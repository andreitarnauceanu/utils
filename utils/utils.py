import os
import boto3
from PIL import Image
from boto3.s3.transfer import S3Transfer
import json
import requests

GOOGLE_URL_SHORTEN_API = 'AIzaSyBrnkM64WKqmKa_FmRbR6WIZeAu-hXE-6I' # IP Address restrictions

def shorten(url):
   req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + GOOGLE_URL_SHORTEN_API
   payload = {'longUrl': url}
   headers = {'content-type': 'application/json'}
   r = requests.post(req_url, data=json.dumps(payload), headers=headers)
   resp = json.loads(r.text)
   return resp['id']

def pre_signed_url(key, bucket):
        s3Client = boto3.client('s3')
        return s3Client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': key}, ExpiresIn = 300)

def crop(image_path, coords, saved_location):
  """
  @param image_path: The path to the image to edit
  @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
  @param saved_location: Path to save the cropped image
  """
  image_obj = Image.open(image_path)
  cropped_image = image_obj.crop(coords)
  cropped_image.save(saved_location)
  cropped_image.show()

def uploadfile(sourcefile, bucket_name, folder):
  """
  @param sourcefile: Filename to be uploaded
  @param bucket_name: S3 bucket name
  @param folder: Path to upload the file
  """
  s3 = boto3.client('s3',)
  filename = sourcefile.split('/')[-1]
  transfer = S3Transfer(s3)
  data = open(sourcefile, 'rb')
  transfer.upload_file(sourcefile , bucket_name, '{}/{}'.format(folder, filename))
  
def removefile(sourcefile):
  os.remove(sourcefile)


def downloadfile(bucket_name, dst_folder, filepath):
  """
  @param bucket_name: S3 bucket name
  @param dst_folder: Folder to download file
  @param filepath: S3 Filepath
  """
#  client = boto3.client('s3',)
#  transfer = S3Transfer(client)
#  # Download s3://bucket/key to ./folder/myfile
#  transfer.download_file(bucket_name, filepath, '{}/{}'.format(dst_folder,filepath.split('/')[-1]))
  s3 = boto3.resource('s3')
  if not os.path.exists(dst_folder):
    os.mkdir(dst_folder)
  bucket = s3.Bucket(bucket_name)
  filename = filepath.split('/')[-1]
  with open('{}/{}'.format(dst_folder, filename), 'wb') as data:
    bucket.download_fileobj(filepath, data)


