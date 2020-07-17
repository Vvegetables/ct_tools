from ct_tools.django_utils.utils.excel_tools.loader import excel_loader
if __name__ == "__main__":
    print(
        excel_loader(r"C:\Users\Zcxu\Desktop\单位不存在.xlsx", True)
    )