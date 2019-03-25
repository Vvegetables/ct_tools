from setuptools import setup,find_packages

setup(
	name = "ct_tools",
	version = "0.0.7",
	description = "ct tools",
	author = "Vvegetables",
	author_email = "hardwork_fight@163.com",
	license = "Public domain",
	url = "https://github.com/Vvegetables/ct_tools",
	packages = find_packages(),
	platforms = ["all"],
	install_requires = [
		"Django >= 1.11.0, < 2.0",
		"PyMysql >= 0.9.2",
	],
	classifiers = [
		"Development Status :: 2 - Pre-Alpha",
		"Environment :: Web Environment",
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	include_package_data=True,    # 启用清单文件MANIFEST.in
	exclude_package_date={'':['.gitignore']} #去除部分不想要的文件
)