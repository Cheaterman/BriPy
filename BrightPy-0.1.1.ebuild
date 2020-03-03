# Copyright 1999-2018 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

PYTHON_COMPAT=( python{2_7,3_5,3_6,3_7} )

inherit distutils-r1 git-r3

DESCRIPTION="Control the backlight through sysfs"
HOMEPAGE="https://github.com/Cheaterman/BriPy"
EGIT_REPO_URI="https://github.com/Cheaterman/BriPy"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""

DEPEND="${PYTHON_DEPS}"
RDEPEND="${DEPEND}"
