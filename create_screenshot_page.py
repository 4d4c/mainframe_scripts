import sys
import glob

name = ""
if len(sys.argv) > 2:
    name = "_clean"

with open("./html/" + sys.argv[1] + "_super" + name + ".html", "w") as html_file:
    header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SUPER HTML</title>
        <style type="text/css">
            .holder{
                width:  590px;
                height: 385px;
                position: relative;
                padding-bottom: 20px;
                display: inline-block;
            }
            .frame{
                width:  590px;
                height: 385px;
                padding-top: 20px;
            }
            .bar{
                position: absolute;
                top: 0;
                left: 220px;
                width: 385px;
                height: 70px;
            }
        </style>
    </head>
    <body>
    """
    html_file.write(header)

    for filename in glob.glob("./html/{}/*.html".format(sys.argv[1])):
        if "super" in filename:
            continue

        div = '<div class="holder"> <div class="bar">{}</div> <div class="frame">{}</div> </div>â€‹'
        with open(filename, "r")as screenshot_file:
            data = screenshot_file.read()

        if len(sys.argv) > 2:
            if "ERROR CODE" not in data and "ERROR CODE" not in data and "ERROR CODE" not in data:
                html_file.write(div.format(filename.split("/")[-1].split(".")[0], data))
        else:
            html_file.write(div.format(filename.split("/")[-1].split(".")[0], data))

    footer = """
    </body>
    </html>
    """
    html_file.write(footer)
