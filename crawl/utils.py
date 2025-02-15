def save_to_file(content, filename="C:/Users/Dantae/log_output.txt"):
    try:
        with open(filename, "a", encoding="utf-8") as file:  # "a" 모드는 파일에 내용을 추가
            file.write(content + "\n")
        print(f"내용이 '{filename}'에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")