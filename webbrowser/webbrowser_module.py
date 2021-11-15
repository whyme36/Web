import webbrowser as wb
import time


def main(sites='webbrowser_sites.txt'):
    with open(sites,'r', encoding='utf-8') as sites:
        try :
            for site in sites.readlines():
                wb.open_new_tab(site)
                time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
