import paramiko
import logging
import time
import re

class SSHConnection():
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    def connect(self):
        try:
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
            self.channel = self.client.invoke_shell()
            print(f"{self.hostname}に接続しました。")
        except paramiko.AuthenticationException:
            print("認証に失敗しました。ユーザー名とパスワードを確認してください。")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH接続エラー: {ssh_exception}")   
    
    def test_connectiion(self,pattern):
        try:
            self.channel.send('cd source_code'+ "\n")
            self.channel.send('ls'+ "\n")
            output = self.recv_all(2)
            filteroutput = self.extract_all_host_blocks(output, pattern)
            lastoutput = self.remove_ansi_escape(filteroutput)
        finally:
            self.channel.close()
            self.client.close()
            print("接続を閉じます") 
            return lastoutput
        
    def recv_all(self, timeout = 2):
        """全ての出力を受信するメソッド"""
        # 出力を受信（バッファサイズ1024バイトずつ）
        start_time = time.time()
        output = ""
        while True:
           if self.channel.recv_ready():
               output += self.channel.recv(1024).decode('utf-8')
           elif time.time() - start_time > timeout:
               break
           else:
               time.sleep(0.1)
        # 行単位で処理
        #for line in output.splitlines():
        #    print(line.strip())
        return output
    
    def extract_all_host_blocks(self,output, pattern):
        matches = list(re.finditer(pattern, output))
        if len(matches) < 2:
            return ""  # 2つ以上ない場合は何も返さない
    
        result = []
        for i in range(1, len(matches)):  # 2個目のmatchから開始
            start = matches[i].start()
            end = matches[i+1].start() if i+1 < len(matches) else len(output)
            block = output[start:end].strip()
            result.append(block)  # 各ブロックの前に改行を入れる
    
        return "".join(result)
    
    def remove_ansi_escape(self,text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
       
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    hostname = "raspi-a"
    username = "raspi-a"
    password = "9574"
    sshconnection = SSHConnection(hostname, username, password)
    sshconnection.connect()
    sshconnection.test_connectiion()