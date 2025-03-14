def MENGIRIMKAN_TAMPILAN(self, video_form, post_action, video_url, action_type="views"):
    global SUKSES, GAGAL
    with requests.Session() as session:
        boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        session.headers.update({
            'User-Agent': get_random_user_agent(),
            'Cookie': f'{COOKIES["Cookie"]}; {self.BYPASS_IKLAN_GOOGLE()}; window_size=1280x551; user_agent={urllib.parse.quote(get_random_user_agent())}; language=en-US; languages=en-US; time_zone=Asia/Jakarta; cf-locale=en-US;',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Origin': 'https://zefoy.com',
            'Sec-Fetch-Dest': 'empty',
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Accept': '*/*'
        })
        proxies = get_random_proxy()
        data = MultipartEncoder({video_form: (None, video_url)}, boundary=boundary)
        response = session.post(f'https://zefoy.com/{post_action}', data=data, proxies=proxies).text
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
            
            # Chờ 4 phút trước khi gửi POST tiếp theo
            printf(f"[bold bright_white]   ──>[bold green] WAITING 4 MINUTES BEFORE NEXT REQUEST...          ", end='\r')
            self.DELAY(4, 0)  # Chờ 4 phút (240 giây)

            data = MultipartEncoder({
                self.form_videoid: (None, self.videoid),
                self.form_videolink: (None, self.videolink)
            }, boundary=boundary)
            response2 = session.post(f'https://zefoy.com/{self.next_post_action}', data=data, proxies=proxies).text
            self.base64_string2 = self.DECRYPTION_BASE64(response2)

            if action_type == "views":
                if 'Successfully 1000 views sent.' in str(self.base64_string2):
                    with LOCK:
                        SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Views :[bold yellow] +1000""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
                elif 'Successfully ' in str(self.base64_string2) and ' views sent.' in str(self.base64_string2):
                    self.views_sent = re.search(r'Successfully (.*?) views sent.', str(self.base64_string2)).group(1)
                    with LOCK:
                        SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold yellow] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Views :[bold green] +{self.views_sent}""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    # Chờ 1 phút trước khi gửi lần hoàn chỉnh tiếp theo
                    printf(f"[bold bright_white]   ──>[bold green] WAITING 1 MINUTE BEFORE NEXT SEND...          ", end='\r')
                    self.DELAY(1, 0)  # Chờ 1 phút (60 giây)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
                else:
                    with LOCK:
                        GAGAL.append(f"{self.base64_string2}")
                    printf(f"[bold bright_white]   ──>[bold red] FAILED TO SEND VIEWS!           ", end='\r')
                    time.sleep(3.5)
                    with LOCK:
                        COOKIES.update({"Cookie": None})
                    return False
            elif action_type == "hearts":
                if '10+ Hearts successfully sent.' in str(self.base64_string2):
                    with LOCK:
                        SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Hearts :[bold yellow] +10""", width=56, style="bold bright_white", title="[bold bright_white][ Sukses ]"))
                    printf(f"[bold bright_white]   ──>[bold green] TRY SENDING HEARTS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    # Chờ 1 phút trước khi gửi lần hoàn chỉnh tiếp theo
                    printf(f"[bold bright_white]   ──>[bold green] WAITING 1 MINUTE BEFORE NEXT SEND...          ", end='\r')
                    self.DELAY(1, 0)  # Chờ 1 phút (60 giây)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
                else:
                    with LOCK:
                        GAGAL.append(f"{self.base64_string2}")
                    printf(f"[bold bright_white]   ──>[bold red] FAILED TO SEND HEARTS!           ", end='\r')
                    time.sleep(3.5)
                    with LOCK:
                        COOKIES.update({"Cookie": None})
                    return False
        elif 'Checking Timer...' in str(self.base64_string):
            printf(f"[bold bright_white]   ──>[bold green] WAIT FOR 4 MINUTES!          ", end='\r')
            time.sleep(2.5)
            list(map(lambda _: (self.DELAY(0, 30), self.ANTI_LOGOUT()), range(8)))
            printf(f"[bold bright_white]   ──>[bold green] TRY SENDING {action_type.upper()} AGAIN!           ", end='\r')
            time.sleep(2.5)
            self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
        elif 'Please try again later or' in str(self.base64_string):
            printf(f"[bold bright_white]   ──>[bold red] PLEASE TRY AGAIN IN A FEW MOMENTS!     ", end='\r')
            time.sleep(2.5)
            self.DELAY(0, 300)
            return False
        elif 'Please try again later. Server too busy.' in str(self.base64_string):
            printf(Panel(f"[bold red]Zefoy server is busy...", width=56, style="bold bright_white", title="[bold bright_white][ Server Sibuk ]"))
            sys.exit()
        elif 'An error occurred. Please try again.' in str(self.base64_string):
            printf(f"[bold bright_white]   ──>[bold red] AN ERROR OCCURRED...", end='\r')
            time.sleep(2.5)
            self.DELAY(0, 120)
            return False
        elif 'Too many requests. Please slow down.' in str(self.base64_string):
            printf(f"[bold bright_white]   ──>[bold red] SUBJECT TO SPAM OR LIMIT!           ", end='\r')
            time.sleep(2.5)
            self.DELAY(0, 500)
            return False
        elif 'Please wait ' in str(self.base64_string) and ' seconds before trying again.' in str(self.base64_string):
            self.wait_time = re.search(r'Please wait (.*?) seconds before trying again.', str(self.base64_string)).group(1)
            printf(f"[bold bright_white]   ──>[bold red] PLEASE WAIT {self.wait_time} SECONDS...", end='\r')
            time.sleep(2.5)
            self.DELAY(0, int(self.wait_time))
            printf(f"[bold bright_white]   ──>[bold green] TRY SENDING {action_type.upper()} AGAIN!           ", end='\r')
            time.sleep(2.5)
            self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url, action_type)
        else:
            printf(f"[bold bright_white]   ──>[bold red] FAILED TO GET {action_type.upper()} FORM!     ", end='\r')
            time.sleep(3.5)
            with LOCK:
                COOKIES.update({"Cookie": None})
            return False
