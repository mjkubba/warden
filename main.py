import hcl


def main():
    with open('../tf-s3/main.tf', 'r') as fp:
        obj = hcl.load(fp)
        print(obj)



if __name__ == "__main__":
    main()
