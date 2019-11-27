// SPDX-License-Identifier: GPL-2.0-only

/*
 * Copyright (C) 2017 Datto Inc.
 * Additional contributions by Assurio Software, Inc are Copyright (C) 2019 Assurio Software Inc.
 */

#include "includes.h"

static inline void dummy(void){
	struct file *f = NULL;
	const void *buf = NULL;
	loff_t *pos = NULL;

	(void)kernel_write(f, buf, 0, pos);
}
