from datetime import datetime


def make_page(contents, content_length=100):
    print("start make page")
    template_datatable = None
    with open("template/datatable.html", "r", encoding="utf-8", errors="ignore") as f:
        template_datatable = f.read()

    randerText = None
    with open("template/rander.html", "r", encoding="utf-8", errors="ignore") as f:
        randerText = f.read()

    data_list = []
    for c in contents:
        """
        <tr>
            <td>{newsTitle}</td>
            <td><a href="{newsLink}">{newsDetail}</a></td>
        </tr>
        """
        description = ""
        if "detail" in c.keys():
            print(c["detail"])
            if isinstance(c["detail"], dict):
                description = c["detail"]["description"]
                if len(description) > content_length:
                    description = description[:content_length] + "..."
        datatable = template_datatable.format(
            newsTitle=c["title"],
            newsDate=c["date"],
            newsLink=c["link"],
            newsDetail=description,
        )
        data_list.append(datatable)
    print(data_list)
    today = datetime.strftime(datetime.now(), "%Y-%m-%d")
    randerText = randerText.format(Date=today, datatable="\n".join(data_list))
    with open("pages/index.html", "w", encoding="utf-8") as w:
        w.write(randerText)

    print("make compelte...!")
