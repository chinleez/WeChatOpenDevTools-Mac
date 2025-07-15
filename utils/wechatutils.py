import os,re,sys
import psutil,subprocess
from utils.colors import Color
import subprocess
import time
class WechatUtils:
    version_command = "ps aux | grep 'WeChatAppEx' |  grep -v 'grep' | grep ' --client_version' | grep '-user-agent=' | grep -oE 'MacWechat/[0-9]+\.[0-9]+\.[0-9]+\(0x[0-9a-f]+\)' |  grep -oE '0x[0-9a-f]+' | sed 's/0x//g' | head -n 1"
    def __init__(self):
        self.configs_path = self.get_configs_path()
        self.version_list = self.get_version_list()
        if sys.platform.startswith('win'):
            import winreg 
        else:
            winreg = None
            
        # self.pid , self.version =  self.get_wechat_pid_and_version()
        # if self.pid is None and self.version is None:
        #     self.print_process_not_found_message()

    def get_configs_path(self):
        current_path = os.path.abspath(__file__)
        relative_path = '../configs/'
        return os.path.join(os.path.dirname(current_path), relative_path)

    def get_version_list(self):
        configs_path = self.configs_path
        version_list = os.listdir(configs_path)
        versions_list = [file.split('_')[1] for file in version_list if file.startswith('address_')]
        return versions_list

    def is_wechatEx_process(self, cmdline):
        process_name = "WeChatAppEx"
        return cmdline and process_name in cmdline[0] and "--type=" not in ' '.join(cmdline)


    def extract_version_number(self, cmdline):
        str = ' '.join(cmdline)
        version_match = re.search(r'"version":(\d+)', str)
        return int(version_match.group(1)) if version_match else None
    
    def get_wechat_pid_and_version(self):
        processes = (proc.info for proc in psutil.process_iter(['pid', 'cmdline']))	
        wechatEx_processes = (p for p in processes if self.is_wechatEx_process(p['cmdline']))
        for process in wechatEx_processes:
            pid = process['pid']
            version = self.extract_version_number(process['cmdline'])
            if version in self.version_list:
                return pid, version
        
        return None, None
    
    def print_process_not_found_message(self):
        print(Color.RED + "[-] 未找到匹配版本的微信进程或微信未运行" + Color.END)

    import subprocess
    import time
    from utils.colors import Color

    def get_wechat_pid_and_version_mac(self):
        """获取微信进程ID和版本号，若未找到则持续等待"""
        wait_interval = 3  # 重试间隔(秒)
        max_attempts = 30  # 最大尝试次数

        for attempt in range(max_attempts):
            try:
                # 查找微信进程PID
                pid_command = "ps aux | grep 'WeChatAppEx' |  grep -v 'grep' | grep ' --client_version' | grep '-user-agent=' | awk '{print $2}' | tail -n 1"
                pid_result = subprocess.run(
                    pid_command,
                    shell=True,
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                pid = pid_result.stdout.strip()

                if not pid:
                    raise ValueError("未找到微信进程")

                # 查找微信版本号
                version_result = subprocess.run(
                    self.version_command,
                    shell=True,
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                version = version_result.stdout.strip()

                if not version:
                    raise ValueError("无法获取微信版本")

                print(Color.GREEN + f"[+] 查找到微信的PID是：{pid}" + Color.END)
                print(Color.GREEN + f"[+] 查找到微信的版本是：{version}" + Color.END)
                return int(pid), version

            except (subprocess.CalledProcessError, ValueError) as e:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(Color.YELLOW +
                          f"[-] 未找到微信进程，{wait_interval}秒后重试 ({remaining}次剩余)" +
                          Color.END)
                    time.sleep(wait_interval)
                else:
                    print(Color.RED +
                          f"[!] 尝试超时：未能找到微信进程或获取版本号" +
                          Color.END)
                    return None, None

            except Exception as e:
                print(Color.RED +
                      f"[!] 查找微信进程时发生未知错误：{str(e)}" +
                      Color.END)
                return None, None

        return None, None  # 所有尝试失败后返回
    def get_wechat_version_mac(self):
        try:
            version  = subprocess.run(self.version_command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.replace("\n","")
            print(Color.GREEN + f"[+] 查找到微信的版本是：{version}" + Color.END)
            return version
        except subprocess.CalledProcessError as e:
            return e.stderr
