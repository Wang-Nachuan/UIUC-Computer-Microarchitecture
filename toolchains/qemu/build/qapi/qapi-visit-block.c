/* AUTOMATICALLY GENERATED, DO NOT MODIFY */

/*
 * Schema-defined QAPI visitors
 *
 * Copyright IBM, Corp. 2011
 * Copyright (C) 2014-2018 Red Hat, Inc.
 *
 * This work is licensed under the terms of the GNU LGPL, version 2.1 or later.
 * See the COPYING.LIB file in the top-level directory.
 */

#include "qemu/osdep.h"
#include "qapi/error.h"
#include "qapi/qmp/qerror.h"
#include "qapi-visit-block.h"

void visit_type_BiosAtaTranslation(Visitor *v, const char *name, BiosAtaTranslation *obj, Error **errp)
{
    int value = *obj;
    visit_type_enum(v, name, &value, &BiosAtaTranslation_lookup, errp);
    *obj = value;
}

void visit_type_FloppyDriveType(Visitor *v, const char *name, FloppyDriveType *obj, Error **errp)
{
    int value = *obj;
    visit_type_enum(v, name, &value, &FloppyDriveType_lookup, errp);
    *obj = value;
}

void visit_type_PRManagerInfo_members(Visitor *v, PRManagerInfo *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "id", &obj->id, &err);
    if (err) {
        goto out;
    }
    visit_type_bool(v, "connected", &obj->connected, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_PRManagerInfo(Visitor *v, const char *name, PRManagerInfo **obj, Error **errp)
{
    Error *err = NULL;

    visit_start_struct(v, name, (void **)obj, sizeof(PRManagerInfo), &err);
    if (err) {
        goto out;
    }
    if (!*obj) {
        goto out_obj;
    }
    visit_type_PRManagerInfo_members(v, *obj, &err);
    if (err) {
        goto out_obj;
    }
    visit_check_struct(v, &err);
out_obj:
    visit_end_struct(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_PRManagerInfo(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_PRManagerInfoList(Visitor *v, const char *name, PRManagerInfoList **obj, Error **errp)
{
    Error *err = NULL;
    PRManagerInfoList *tail;
    size_t size = sizeof(**obj);

    visit_start_list(v, name, (GenericList **)obj, size, &err);
    if (err) {
        goto out;
    }

    for (tail = *obj; tail;
         tail = (PRManagerInfoList *)visit_next_list(v, (GenericList *)tail, size)) {
        visit_type_PRManagerInfo(v, NULL, &tail->value, &err);
        if (err) {
            break;
        }
    }

    if (!err) {
        visit_check_list(v, &err);
    }
    visit_end_list(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_PRManagerInfoList(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_q_obj_eject_arg_members(Visitor *v, q_obj_eject_arg *obj, Error **errp)
{
    Error *err = NULL;

    if (visit_optional(v, "device", &obj->has_device)) {
        visit_type_str(v, "device", &obj->device, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "id", &obj->has_id)) {
        visit_type_str(v, "id", &obj->id, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "force", &obj->has_force)) {
        visit_type_bool(v, "force", &obj->force, &err);
        if (err) {
            goto out;
        }
    }

out:
    error_propagate(errp, err);
}

void visit_type_q_obj_blockdev_open_tray_arg_members(Visitor *v, q_obj_blockdev_open_tray_arg *obj, Error **errp)
{
    Error *err = NULL;

    if (visit_optional(v, "device", &obj->has_device)) {
        visit_type_str(v, "device", &obj->device, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "id", &obj->has_id)) {
        visit_type_str(v, "id", &obj->id, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "force", &obj->has_force)) {
        visit_type_bool(v, "force", &obj->force, &err);
        if (err) {
            goto out;
        }
    }

out:
    error_propagate(errp, err);
}

void visit_type_q_obj_blockdev_close_tray_arg_members(Visitor *v, q_obj_blockdev_close_tray_arg *obj, Error **errp)
{
    Error *err = NULL;

    if (visit_optional(v, "device", &obj->has_device)) {
        visit_type_str(v, "device", &obj->device, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "id", &obj->has_id)) {
        visit_type_str(v, "id", &obj->id, &err);
        if (err) {
            goto out;
        }
    }

out:
    error_propagate(errp, err);
}

void visit_type_q_obj_blockdev_remove_medium_arg_members(Visitor *v, q_obj_blockdev_remove_medium_arg *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "id", &obj->id, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_q_obj_blockdev_insert_medium_arg_members(Visitor *v, q_obj_blockdev_insert_medium_arg *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "id", &obj->id, &err);
    if (err) {
        goto out;
    }
    visit_type_str(v, "node-name", &obj->node_name, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_BlockdevChangeReadOnlyMode(Visitor *v, const char *name, BlockdevChangeReadOnlyMode *obj, Error **errp)
{
    int value = *obj;
    visit_type_enum(v, name, &value, &BlockdevChangeReadOnlyMode_lookup, errp);
    *obj = value;
}

void visit_type_q_obj_blockdev_change_medium_arg_members(Visitor *v, q_obj_blockdev_change_medium_arg *obj, Error **errp)
{
    Error *err = NULL;

    if (visit_optional(v, "device", &obj->has_device)) {
        visit_type_str(v, "device", &obj->device, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "id", &obj->has_id)) {
        visit_type_str(v, "id", &obj->id, &err);
        if (err) {
            goto out;
        }
    }
    visit_type_str(v, "filename", &obj->filename, &err);
    if (err) {
        goto out;
    }
    if (visit_optional(v, "format", &obj->has_format)) {
        visit_type_str(v, "format", &obj->format, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "read-only-mode", &obj->has_read_only_mode)) {
        visit_type_BlockdevChangeReadOnlyMode(v, "read-only-mode", &obj->read_only_mode, &err);
        if (err) {
            goto out;
        }
    }

out:
    error_propagate(errp, err);
}

void visit_type_q_obj_DEVICE_TRAY_MOVED_arg_members(Visitor *v, q_obj_DEVICE_TRAY_MOVED_arg *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "device", &obj->device, &err);
    if (err) {
        goto out;
    }
    visit_type_str(v, "id", &obj->id, &err);
    if (err) {
        goto out;
    }
    visit_type_bool(v, "tray-open", &obj->tray_open, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_q_obj_PR_MANAGER_STATUS_CHANGED_arg_members(Visitor *v, q_obj_PR_MANAGER_STATUS_CHANGED_arg *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "id", &obj->id, &err);
    if (err) {
        goto out;
    }
    visit_type_bool(v, "connected", &obj->connected, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_q_obj_block_latency_histogram_set_arg_members(Visitor *v, q_obj_block_latency_histogram_set_arg *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "id", &obj->id, &err);
    if (err) {
        goto out;
    }
    if (visit_optional(v, "boundaries", &obj->has_boundaries)) {
        visit_type_uint64List(v, "boundaries", &obj->boundaries, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "boundaries-read", &obj->has_boundaries_read)) {
        visit_type_uint64List(v, "boundaries-read", &obj->boundaries_read, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "boundaries-write", &obj->has_boundaries_write)) {
        visit_type_uint64List(v, "boundaries-write", &obj->boundaries_write, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "boundaries-flush", &obj->has_boundaries_flush)) {
        visit_type_uint64List(v, "boundaries-flush", &obj->boundaries_flush, &err);
        if (err) {
            goto out;
        }
    }

out:
    error_propagate(errp, err);
}

/* Dummy declaration to prevent empty .o file */
char qapi_dummy_qapi_visit_block_c;
