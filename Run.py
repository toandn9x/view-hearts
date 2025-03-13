def MENGIRIMKAN_TAMPILAN(self, video_form, post_action, video_url, action_type="views"):
    global SUKSES, GAGAL
    with requests.Session() as session:
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

        boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        data = MultipartEncoder({video_form: (None, video_url)}, boundary=boundary)
        response = session.post(f'https://zefoy.com/{post_action}', data=data).text
        self.base64_string = self.DECRYPTION_BASE64(response)

        if 'type="submit"' in str(self.base64_string):
            boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            session.headers.update({'Content-Type': f'multipart/form-data; boundary={boundary}'})
            self.find_form_video = re.findall(r'type="hidden" name="(.*?)" value="(.*?)"', str(self.base64_string))
            if len(self.find_form_video) >= 2:
                self.form_videolink, self.videolink = self.find_form_video[1][0], self.find_form_video[1][1]
                self.form_videoid, self.videoid = self.find_form_video[0][0], self.find_form_video[0][1]
            else:
                printf(f"[bold bright_white]   ──>[bold red] UNABLE TO FIND REQUIRED FORM FIELDS!     ", end='\r')
                time.sleep(3.5)
                return False
            self.next_post_action = re.search(r'action="(.*?)"', str(self.base64_string)).group(1)
            data = MultipartEncoder({
                self.form_videoid: (None, self.videoid),
                self.form_videolink: (None, self.videolink)
            }, boundary=boundary)

            response2 = session.post(f'https://zefoy.com/{self.next_post_action}', data=data).text
            self.base64_string2 = self.DECRYPTION_BASE64(response2)

            if action_type == "views":
                if 'Successfully 1000 views sent.' in str(self.base64_string2):
                    SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Views :[bold yellow] +1000""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
                elif 'Successfully ' in str(self.base64_string2) and ' views sent.' in str(self.base64_string2):
                    self.views_sent = re.search(r'Successfully (.*?) views sent.', str(self.base64_string2)).group(1)
                    SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold yellow] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Views :[bold green] +{self.views_sent}""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
                else:
                    GAGAL.append(f"{self.base64_string2}")
                    printf(f"[bold bright_white]   ──>[bold red] FAILED TO SEND VIEWS!           ", end='\r')
                    time.sleep(3.5)
                    COOKIES.update({"Cookie": None})
                    return False
            elif action_type == "hearts":
                if 'Successfully ' in str(self.base64_string2) and ' hearts sent.' in str(self.base64_string2):
                    self.hearts_sent = re.search(r'Successfully (.*?) hearts sent.', str(self.base64_string2)).group(1)
                    SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Hearts :[bold yellow] +{self.hearts_sent}""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING HEARTS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
                else:
                    GAGAL.append(f"{self.base64_string2}")
                    printf(f"[bold bright_white]   ──>[bold red] FAILED TO SEND HEARTS!           ", end='\r')
                    time.sleep(3.5)
                    COOKIES.update({"Cookie": None})
                    return False
        # Các điều kiện lỗi khác giữ nguyên
