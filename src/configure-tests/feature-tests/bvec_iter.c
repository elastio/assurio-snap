// SPDX-License-Identifier: GPL-2.0-only

/*
 * Copyright (C) 2015 Datto Inc.
 * Additional contributions by Assurio Software, Inc are Copyright (C) 2019 Assurio Software Inc.
 */

#include "includes.h"

static inline void dummy(void){
	struct bvec_iter iter;
	if(iter.bi_sector) iter.bi_sector = 0;
}
