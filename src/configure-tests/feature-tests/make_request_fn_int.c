// SPDX-License-Identifier: GPL-2.0-only

/*
 * Copyright (C) 2015 Datto Inc.
 * Additional contributions by Assurio Software, Inc are Copyright (C) 2019 Assurio Software Inc.
 */

#include "includes.h"

static int dummy_mrf(struct request_queue *q, struct bio *bio){
	return 0;
}

static inline void dummy(void){
	struct bio b;
	struct request_queue q = {
		.make_request_fn = dummy_mrf,
	};

	q.make_request_fn(&q, &b);
}
