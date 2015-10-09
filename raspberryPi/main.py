import bibus

def main():
    b = bibus.Bibus()

    print(b.getVersion()[0])

if __name__=="__main__":
    main()
