all:
	rpmdev-setuptree
	spectool -g -R aprx.spec
	rpmbuild -bb aprx.spec
