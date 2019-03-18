from setuptools import setup,find_packages

setup(
	name = 'ct_tools',
	version = "0.0.1",
	packages = find_packages(),
	include_package_data=True,    # 启用清单文件MANIFEST.in
	exclude_package_date={'':['.gitignore']}, #去除部分不想要的文件
	descrition="personal use",
	author ="Vvegetables",
	url="https://github.com/Vvegetables/ct_tools",
	author_email="hardwork_fight@163.com",
	license="Public domain",
	install_require=[
		"PyMysql>=0.9.2",
		"Django>=1.11.5",
	],
)