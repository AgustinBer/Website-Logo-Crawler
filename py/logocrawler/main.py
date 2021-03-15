import sys

def main():
    data = sys.stdin.read() 
    urls = data.split('\n')
    print(urls)
        
if __name__=="__main__": 
    main()