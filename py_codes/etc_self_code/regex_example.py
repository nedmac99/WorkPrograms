import re


def main():
    print(parse(input("HTML: ")))


def parse(url):
    pattern = r'src="https?://(?:www\.)?(?:youtube\.com/embed/|youtu\.be/)(\w+-*)"'
    link = re.search(pattern, url)
    if link:
        video_id = link.group(1)
        return f"https://youtu.be/{video_id}"
    else:
        return "None"


if __name__ == "__main__":
    main()
