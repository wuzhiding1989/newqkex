from common.mysql_san import mysql_select


class GenerateEmailTemplate:
    """
    1、获取内容模板
    2、替换内容模板
    3、替换邮件模板
    """

    def get_bg_template(self,templatekey):

        """

        :param template_key: DEFAULT_SUBJECT 英文模板；DEFAULT_SUBJECT_ZH_CN 中文模板
        :return:
        """
        sql =f"select template_content from foundation.integration_message_bg_template where template_key= '{templatekey}';"
        data = mysql_select(sql,ac=3)
        return data
    def get_template(self):
        """
        获取内容模板
        :return:
        """
        sql = f"select id,code,sign,subject,locale,type,content,create_on,update_on from foundation.integration_message_template ;"
        data = mysql_select(sql, ac=3)
        return data

    def replaceString(self,string: str):
        if "${remark}" in string:
            string = string.replace("${remark}",
                                    "The certificate does not meet the verification requirements, please select the correct nationality for verification.")
        if "${id}" in string:
            string = string.replace("${id}", "1478")
        if "${totalPrice}" in string:
            string = string.replace("${totalPrice}", "20291.82")
        if "${legalSymbol}" in string:
            string = string.replace("${legalSymbol}", "USD")
        if "${number}" in string:
            string = string.replace("${number}", "0.1")
        if "${symbol}" in string:
            string = string.replace("${symbol}", "BTC")
        if "${minute}" in string:
            string = string.replace("${minute}", "15 minutes")
        if "${unitPrice}" in string:
            string = string.replace("${unitPrice}", "20291.82")
        if "${reason}" in string:
            string = string.replace("${reason}", "The handheld ID photo does not match the front photo of the ID")

        # if "${totalPrice}" in string:
        # string.replace("${totalPrice}","20291.82")
        # if "${legalSymbol}" in string:
        #     string.replace("${legalSymbol}","USD")
        return string

    def generate(self):

        data=self.get_template()#内容模板
        for item in data:
            id=item[0]
            code=item[1]
            sign=item[2]
            subject=item[3]
            locale=item[4]
            type=item[5]
            content=item[6]
            create_on=item[6]
            update_on=item[6]
            content=self.replaceString(content)
            if locale=="zh-cn" or locale=="zh-hk":
                template_key="DEFAULT_SUBJECT_ZH_CN"
                language="中文"
            else:
                template_key = "DEFAULT_SUBJECT"
                language = "英文"
            bg_template = self.get_bg_template(template_key)[0][0]
            html_data = bg_template.replace("${subject}", subject).replace("${content}", content)
            with open(file="./email/" + "数据库模板ID：" + str(id)+"_" +str(code)+ language+".html", mode="w",
                      encoding="UTF-8") as f:
                f.write(html_data)
                f.close()

if __name__ == '__main__':
    GenerateEmailTemplate().generate()
    # template_key = "DEFAULT_SUBJECT"
    # data=GenerateEmailTemplate().get_bg_template(template_key)[0][0]
    # print(type(data))
