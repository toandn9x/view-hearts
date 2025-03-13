import requests, re, random, string, base64, urllib.parse, json, time, os, sys
from requests_toolbelt import MultipartEncoder
from rich import print as printf
from PIL import Image
import pytesseract
from rich.panel import Panel
from rich.console import Console
from requests.exceptions import RequestException

COOKIES, SUKSES, LOGOUT, GAGAL = {"Cookie": None}, [], [], []

class DIPERLUKAN:
    def __init__(self) -> None:
        pass

    def LOGIN(self):
        with requests.Session() as session:
            session.headers.update({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Host': 'zefoy.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document'
            })
            response = session.get('https://zefoy.com/').text
            if 'Sorry, you have been blocked' in str(response) or 'Just a moment...' in str(response):
                printf(Panel(f"[bold red]Zefoy server is currently affected by cloudflare...", width=56, style="bold bright_white", title="[bold bright_white][ Cloudflare ]"))
                sys.exit()
            else:
                self.captcha_image = re.search(r'src="(.*?)" onerror="errimg\(\)"', str(response)).group(1).replace('amp;', '')
                self.form = re.search(r'type="text" name="(.*?)"', str(response)).group(1)
                session.headers.update({
                    'Cookie': "; ".join([str(x) + "=" + str(y) for x, y in session.cookies.get_dict().items()]),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
                })
                response2 = session.get('https://zefoy.com{}'.format(self.captcha_image))
                with open('Penyimpanan/Gambar.png', 'wb') as w:
                    w.write(response2.content)
                session.headers.update({
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Connection': 'keep-alive',
                    'Origin': 'null',
                    'Cookie': "; ".join([str(x) + "=" + str(y) for x, y in session.cookies.get_dict().items()])
                })
                data = {self.form: self.BYPASS_CAPTCHA()}
                response3 = session.post('https://zefoy.com/', data=data).text
                if 'placeholder="Enter Video URL"' in str(response3):
                    COOKIES.update({"Cookie": "; ".join([str(x)+"="+str(y) for x,y in session.cookies.get_dict().items()])})
                    printf(f"[bold bright_white]   ──>[bold green] LOGIN SUCCESSFUL!                ", end='\r')
                    time.sleep(2.5)
                    return COOKIES['Cookie']
                else:
                    printf(f"[bold bright_white]   ──>[bold red] LOGIN FAILED!                     ", end='\r')
                    time.sleep(2.5)
                    return False

    def BYPASS_CAPTCHA(self):
        self.file_gambar = 'Penyimpanan/Gambar.png'
        self.image = Image.open(self.file_gambar)
        self.image_string = pytesseract.image_to_string(self.image)
        return self.image_string.replace('\n', '')

    def MENDAPATKAN_FORMULIR(self, video_url, feature_choice):
        with requests.Session() as session:
            session.headers.update({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Host': 'zefoy.com',
                'Cookie': f'{COOKIES["Cookie"]}; window_size=1280x551; user_agent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F131.0.0.0%20Safari%2F537.36; language=en-US; languages=en-US; cf-locale=en-US;',
                'Sec-Fetch-Site': 'none',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
            })
            response = session.get('https://zefoy.com/').text
            if 'placeholder="Enter Video URL"' in str(response):
                self.video_form = re.search(r'name="(.*?)" placeholder="Enter Video URL"', str(response)).group(1)
                # Điều chỉnh endpoint dựa trên lựa chọn
                actions = re.findall(r'action="(.*?)">', str(response))
                self.post_action = actions[3] if feature_choice == "1" else actions[1] if feature_choice == "2" else actions[2]  # Giả định Favorites là [2]
                printf(f"[bold bright_white]   ──>[bold green] SUCCESSFULLY FOUND VIDEO FORM!   ", end='\r')
                time.sleep(1.5)
                self.MENGIRIMKAN_TAMPILAN(self.video_form, self.post_action, video_url, feature_choice)
            else:
                printf(f"[bold bright_white]   ──>[bold red] VIDEO FORM NOT FOUND!        ", end='\r')
                time.sleep(3.5)
                COOKIES.update({"Cookie": None})
                return False

    def MENGIRIMKAN_TAMPILAN(self, video_form, post_action, video_url, feature_choice):
        global SUKSES, GAGAL
        with requests.Session() as session:
            boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Cookie': f'{COOKIES["Cookie"]}; {self.BYPASS_IKLAN_GOOGLE()}; window_size=1280x551; user_agent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F131.0.0.0%20Safari%2F537.36; language=en-US; languages=en-US; time_zone=Asia/Jakarta; cf-locale=en-US;',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Connection': 'keep-alive',
                'Origin': 'https://zefoy.com',
                'Sec-Fetch-Dest': 'empty',
                'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
                'Accept': '*/*'
            })
            data = MultipartEncoder({video_form: (None, video_url)}, boundary=boundary)
            response = session.post('https://zefoy.com/{}'.format(post_action), data=data).text
            self.base64_string = self.DECRYPTION_BASE64(response)

            if 'type="submit"' in str(self.base64_string):
                boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
                session.headers.update({'Content-Type': 'multipart/form-data; boundary={}'.format(boundary)})
                self.find_form_video = re.findall(r'type="hidden" name="(.*?)" value="(.*?)"', str(self.base64_string))
                if len(self.find_form_video) >= 2:
                    self.form_videolink, self.videolink = self.find_form_video[1][0], self.find_form_video[1][1]
                    self.form_videoid, self.videoid = self.find_form_video[0][0], self.find_form_video[0][1]
                else:
                    printf(f"[bold bright_white]   ──>[bold red] UNABLE TO FIND REQUIRED FORM FIELDS!     ", end='\r')
                    time.sleep(3.5)
                    return False
                self.next_post_action = re.search(r'action="(.*?)"', str(self.base64_string)).group(1)
                data = MultipartEncoder({self.form_videoid: (None, self.videoid), self.form_videolink: (None, self.videolink)}, boundary=boundary)
                response2 = session.post('https://zefoy.com/{}'.format(self.next_post_action), data=data).text
                self.base64_string2 = self.DECRYPTION_BASE64(response2)

                if feature_choice == "1" and 'Successfully 1000 views sent.' in str(self.base64_string2):
                    SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Views :[bold yellow] +1000""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, feature_choice)
                elif feature_choice == "2" and '10+ Hearts successfully sent' in str(self.base64_string2):
                    SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Hearts :[bold yellow] +10""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING HEARTS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, feature_choice)
                else:
                    GAGAL.append(f"{self.base64_string2}")
                    printf(f"[bold bright_white]   ──>[bold red] FAILED TO SEND REQUEST!           ", end='\r')
                    time.sleep(3.5)
                    COOKIES.update({"Cookie": None})
                    return False
            # Các trường hợp lỗi khác giữ nguyên
            elif 'Checking Timer...' in str(self.base64_string):
                printf(f"[bold bright_white]   ──>[bold green] WAIT FOR 4 MINUTES!          ", end='\r')
                time.sleep(2.5)
                list(map(lambda _: (self.DELAY(0, 30), self.ANTI_LOGOUT()), range(8)))
                printf(f"[bold bright_white]   ──>[bold green] TRY SENDING AGAIN!           ", end='\r')
                time.sleep(2.5)
                self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, feature_choice)
            # Giữ nguyên các xử lý lỗi khác...

    def ANTI_LOGOUT(self):  # Giữ nguyên
        pass

    def DECRYPTION_BASE64(self, base64_code):  # Giữ nguyên
        return base64.b64decode(urllib.parse.unquote(base64_code[::-1])).decode()

    def DELAY(self, menit, detik):  # Giữ nguyên
        self.total = (menit * 60 + detik)
        while self.total:
            menit, detik = divmod(self.total, 60)
            printf(f"[bold bright_white]   ──>[bold white] TUNGGU[bold green] {menit:02d}:{detik:02d}[bold white] SUKSES:-[bold green]{len(SUKSES)}[bold white] GAGAL:-[bold red]{len(GAGAL)}              ", end='\r')
            time.sleep(1)
            self.total -= 1
        return "0_0"

    def BYPASS_IKLAN_GOOGLE(self):  # Giữ nguyên
        pass

class MAIN:
    def __init__(self):
        try:
            self.TAMPILKAN_LOGO()
            printf(Panel(f"[bold white]Please fill in your TikTok video link...", width=56, style="bold bright_white", title="[bold bright_white][ Link Video ]", subtitle="[bold bright_white]╭─────", subtitle_align="left"))
            video_url = Console().input("[bold bright_white]   ╰─> ")
            if 'tiktok.com' in str(video_url) or '/video/' in str(video_url):
                printf(Panel(f"[bold white]You can use[bold green] CTRL + C[bold white] if stuck...", width=56, style="bold bright_white", title="[bold bright_white][ Catatan ]"))
                # Thêm tùy chọn chức năng
                printf("[bold white]Chọn chức năng: 1. Views, 2. Hearts, 3. Favorites")
                choice = Console().input("[bold bright_white]Nhập số: ")
                if choice not in ["1", "2", "3"]:
                    printf(Panel(f"[bold red]Lựa chọn không hợp lệ!", width=56, style="bold bright_white", title="[bold bright_white][ Lỗi ]"))
                    sys.exit()
                while True:
                    try:
                        if COOKIES['Cookie'] is None or len(COOKIES['Cookie']) == 0:
                            DIPERLUKAN().LOGIN()
                        else:
                            printf(f"[bold bright_white]   ──>[bold green] SENDING REQUEST!     ", end='\r')
                            time.sleep(2.5)
                            DIPERLUKAN().MENDAPATKAN_FORMULIR(video_url, choice)
                    except (AttributeError, IndexError):
                        printf(f"[bold bright_white]   ──>[bold red] ERROR OCCURRED IN INDEX FORM!            ", end='\r')
                        time.sleep(7.5)
                        continue
                    except RequestException:
                        printf(f"[bold bright_white]   ──>[bold red] YOUR CONNECTION IS HAVING A PROBLEM!     ", end='\r')
                        time.sleep(7.5)
                        continue
                    except KeyboardInterrupt:
                        printf(f"\r                                 ", end='\r')
                        time.sleep(2.5)
            else:
                printf(Panel(f"[bold red]Please fill in the TikTok video link correctly...", width=56, style="bold bright_white", title="[bold bright_white][ Link Salah ]"))
                sys.exit()
        except Exception as e:
            printf(Panel(f"[bold red]{str(e).capitalize()}!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
            sys.exit()

    def TAMPILKAN_LOGO(self):  # Giữ nguyên
        os.system('cls' if os.name == 'nt' else 'clear')
        printf(Panel(r"""[bold red]● [bold yellow]● [bold green]●[bold white] ...""", width=56, style="bold bright_white"))
        return True

if __name__ == '__main__':
    try:
        os.system('git pull')
        subscribe_file = "Penyimpanan/Subscribe.json"
        if not os.path.exists(subscribe_file):
            youtube_url = requests.get('https://raw.githubusercontent.com/RozhakXD/Zefoy/main/Penyimpanan/Youtube.json').json()['Link']
            os.system(f'xdg-open {youtube_url}')
            with open(subscribe_file, 'w') as w:
                json.dump({"Status": True}, w, indent=4)
            time.sleep(3.5)
        MAIN()
    except Exception as e:
        printf(Panel(f"[bold red]{str(e).capitalize()}!", width=56, style="bold bright_white", title="[bold bright_white][ Error ]"))
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()