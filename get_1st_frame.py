import subprocess
import os

def main(input_file, output_file, frame_quality=5):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vframes', '1',
        '-q:v', str(frame_quality),
        output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Frame extracted and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

src = ''
dest = ''
urls = {}
for root,dirs,files in os.walk(src):
    for file in files:
        if file.lower().endswith('.mov') or file.lower().endswith('.mp4'):
           video_path = os.path.join(root,file)
           img_path = os.path.join(dest,file+'.jpg')
           urls[video_path] = img_path


def main2():
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(main,in_,out_) for in_,out_ in urls.items()]
        for future in concurrent.futures.as_completed(futures):
            future.result() 

if __name__ == '__main__':
    main2()

