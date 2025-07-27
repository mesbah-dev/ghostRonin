import subprocess
import os
import shutil
import sys
from pathlib import Path
def check_tools(tools):
    missing = []
    for tool in tools:
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        print(f"\033[91m[!] Missing required tools: {', '.join(missing)}\033[0m")
        print("[!] Please install them and try again.")
        sys.exit(1)

required_tools = ["subfinder", "assetfinder", "curl", "jq", "sed", "httpx-toolkit", "naabu", "nmap"]
check_tools(required_tools)

def show_banner():
    banner = r"""
	 


 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░   ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░     
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░   ░▒▓█▓▒░     
                                                                   
                                                                   
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░         
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        
                                                                   
                                                                   

                                            

		                                                                               
         🥷 GhostRonin Recon 🥷
                        
	"""
    print(banner)

def print_info(msg):
    print(f"\033[94m{msg}\033[0m")

def print_warning(msg):
    print(f"\033[93m{msg}\033[0m")

def print_error(msg):
    print(f"\033[91m{msg}\033[0m")

def run_command(cmd, output_file=None):
    print_info(f"[*] Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print_error(f"[!] Error running: {cmd}")
    if output_file and not Path(output_file).is_file():
        print_warning(f"[!] Output file not created: {output_file}")

def make_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def filter_subdomains(input_file, output_file, filter_domain):
    with open(input_file, "r") as f:
        subs = f.read().splitlines()
    filtered = [s for s in subs if s.endswith(filter_domain)]
    with open(output_file, "w") as f:
        for s in filtered:
            f.write(s + "\n")

def main(domain, subdomain_filter=None):
    make_dir("nmap_results")

    print_info("\n[1] Finding Subdomains...")
    run_command(f"subfinder -d {domain} -o subfinder.txt", "subfinder.txt")
    run_command(f"assetfinder --subs-only {domain} > assetfinder.txt", "assetfinder.txt")
    run_command(f"curl -s 'https://crt.sh/?q=%25.{domain}&output=json' | jq -r '.[].name_value' | sed 's/\\*\\.//g' | sort -u > crtsh.txt", "crtsh.txt")

    print_info("\n[2] Merging Subdomains...")
    run_command("cat subfinder.txt assetfinder.txt crtsh.txt | sort -u > all_subs.txt", "all_subs.txt")

    if subdomain_filter:
        print_info(f"\n[3] Filtering Subdomains by: {subdomain_filter}")
        filter_subdomains("all_subs.txt", "filtered_subs.txt", subdomain_filter)
        subs_file = "filtered_subs.txt"
    else:
        subs_file = "all_subs.txt"

    print_info("\n[4] Finding Alive Subdomains...")
    run_command(f"httpx-toolkit -l {subs_file} -silent -o alive.txt", "alive.txt")

    print_info("\n[5] Gathering Info on Alive Subdomains...")
    run_command(f"httpx-toolkit -l alive.txt -status-code -title -server -ip -cname -no-color -silent -o alive-info.txt", "alive-info.txt")

    print_info("\n[6] Sorting by Status Code...")
    run_command("grep -E '\\[[2][0-9]{2}\\]' alive-info.txt > 200.txt", "200.txt")
    run_command("grep -E '\\[[3][0-9]{2}\\]' alive-info.txt > 300.txt", "300.txt")
    run_command("grep -E '\\[[4][0-9]{2}\\]' alive-info.txt > 400.txt", "400.txt")
    run_command("grep -E '\\[[5][0-9]{2}\\]' alive-info.txt > 500.txt", "500.txt")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        show_banner()
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        show_banner()
        main(sys.argv[1], sys.argv[2])
    else:
        print_info("Usage: python recon.py <domain> [subdomain_filter]")
        print_info("Example:")
        print_info("  ghostronin target.com")
        print_info("  ghostronin target.com x.target.com")
