from flask import Flask, Response, render_template, request
from os.path import abspath, dirname, join

main_path = dirname(abspath(__file__))
app = Flask(__name__, template_folder=main_path)


@app.route("/", methods=["GET", "POST"])
def miaowu():
    if request.method == "GET":
        return render_template("index.html", miao_str="", wu_str="")
    else:
        if request.form["operation"] == "miao":
            return render_template(
                "index.html",
                miao_str=request.form["miao_str"],
                wu_str=miao(request.form["miao_str"]),
            )
        else:
            return render_template(
                "index.html",
                miao_str=wu(request.form["wu_str"]),
                wu_str=request.form["wu_str"],
            )


def miao(c):
    out = ""
    for i in c:
        p = bin(ord(i))[2:].replace("1", "喵").replace("0", "呜")
        out += (20 - len(p)) * "呜" + p
    return out
    ...


def wu(p):
    out = ""
    buff_i = 0
    for _ in range(len(p) // 20):
        out += chr(
            int(p[buff_i : buff_i + 20].replace("喵", "1").replace("呜", "0"), 2)
        )
        buff_i += 20
    return out
    ...


# print(miao("欸嘿"))
# print(wu(miao("欸嘿")))
if __name__ == "__main__":
    app.run("0.0.0.0", 8131, debug=True)
