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
#include "qapi-visit-control.h"

void visit_type_QMPCapabilityList(Visitor *v, const char *name, QMPCapabilityList **obj, Error **errp)
{
    Error *err = NULL;
    QMPCapabilityList *tail;
    size_t size = sizeof(**obj);

    visit_start_list(v, name, (GenericList **)obj, size, &err);
    if (err) {
        goto out;
    }

    for (tail = *obj; tail;
         tail = (QMPCapabilityList *)visit_next_list(v, (GenericList *)tail, size)) {
        visit_type_QMPCapability(v, NULL, &tail->value, &err);
        if (err) {
            break;
        }
    }

    if (!err) {
        visit_check_list(v, &err);
    }
    visit_end_list(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_QMPCapabilityList(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_q_obj_qmp_capabilities_arg_members(Visitor *v, q_obj_qmp_capabilities_arg *obj, Error **errp)
{
    Error *err = NULL;

    if (visit_optional(v, "enable", &obj->has_enable)) {
        visit_type_QMPCapabilityList(v, "enable", &obj->enable, &err);
        if (err) {
            goto out;
        }
    }

out:
    error_propagate(errp, err);
}

void visit_type_QMPCapability(Visitor *v, const char *name, QMPCapability *obj, Error **errp)
{
    int value = *obj;
    visit_type_enum(v, name, &value, &QMPCapability_lookup, errp);
    *obj = value;
}

void visit_type_VersionTriple_members(Visitor *v, VersionTriple *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_int(v, "major", &obj->major, &err);
    if (err) {
        goto out;
    }
    visit_type_int(v, "minor", &obj->minor, &err);
    if (err) {
        goto out;
    }
    visit_type_int(v, "micro", &obj->micro, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_VersionTriple(Visitor *v, const char *name, VersionTriple **obj, Error **errp)
{
    Error *err = NULL;

    visit_start_struct(v, name, (void **)obj, sizeof(VersionTriple), &err);
    if (err) {
        goto out;
    }
    if (!*obj) {
        goto out_obj;
    }
    visit_type_VersionTriple_members(v, *obj, &err);
    if (err) {
        goto out_obj;
    }
    visit_check_struct(v, &err);
out_obj:
    visit_end_struct(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_VersionTriple(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_VersionInfo_members(Visitor *v, VersionInfo *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_VersionTriple(v, "qemu", &obj->qemu, &err);
    if (err) {
        goto out;
    }
    visit_type_str(v, "package", &obj->package, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_VersionInfo(Visitor *v, const char *name, VersionInfo **obj, Error **errp)
{
    Error *err = NULL;

    visit_start_struct(v, name, (void **)obj, sizeof(VersionInfo), &err);
    if (err) {
        goto out;
    }
    if (!*obj) {
        goto out_obj;
    }
    visit_type_VersionInfo_members(v, *obj, &err);
    if (err) {
        goto out_obj;
    }
    visit_check_struct(v, &err);
out_obj:
    visit_end_struct(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_VersionInfo(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_CommandInfo_members(Visitor *v, CommandInfo *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "name", &obj->name, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_CommandInfo(Visitor *v, const char *name, CommandInfo **obj, Error **errp)
{
    Error *err = NULL;

    visit_start_struct(v, name, (void **)obj, sizeof(CommandInfo), &err);
    if (err) {
        goto out;
    }
    if (!*obj) {
        goto out_obj;
    }
    visit_type_CommandInfo_members(v, *obj, &err);
    if (err) {
        goto out_obj;
    }
    visit_check_struct(v, &err);
out_obj:
    visit_end_struct(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_CommandInfo(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_CommandInfoList(Visitor *v, const char *name, CommandInfoList **obj, Error **errp)
{
    Error *err = NULL;
    CommandInfoList *tail;
    size_t size = sizeof(**obj);

    visit_start_list(v, name, (GenericList **)obj, size, &err);
    if (err) {
        goto out;
    }

    for (tail = *obj; tail;
         tail = (CommandInfoList *)visit_next_list(v, (GenericList *)tail, size)) {
        visit_type_CommandInfo(v, NULL, &tail->value, &err);
        if (err) {
            break;
        }
    }

    if (!err) {
        visit_check_list(v, &err);
    }
    visit_end_list(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_CommandInfoList(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_EventInfo_members(Visitor *v, EventInfo *obj, Error **errp)
{
    Error *err = NULL;

    visit_type_str(v, "name", &obj->name, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_EventInfo(Visitor *v, const char *name, EventInfo **obj, Error **errp)
{
    Error *err = NULL;

    visit_start_struct(v, name, (void **)obj, sizeof(EventInfo), &err);
    if (err) {
        goto out;
    }
    if (!*obj) {
        goto out_obj;
    }
    visit_type_EventInfo_members(v, *obj, &err);
    if (err) {
        goto out_obj;
    }
    visit_check_struct(v, &err);
out_obj:
    visit_end_struct(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_EventInfo(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_EventInfoList(Visitor *v, const char *name, EventInfoList **obj, Error **errp)
{
    Error *err = NULL;
    EventInfoList *tail;
    size_t size = sizeof(**obj);

    visit_start_list(v, name, (GenericList **)obj, size, &err);
    if (err) {
        goto out;
    }

    for (tail = *obj; tail;
         tail = (EventInfoList *)visit_next_list(v, (GenericList *)tail, size)) {
        visit_type_EventInfo(v, NULL, &tail->value, &err);
        if (err) {
            break;
        }
    }

    if (!err) {
        visit_check_list(v, &err);
    }
    visit_end_list(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_EventInfoList(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

void visit_type_MonitorMode(Visitor *v, const char *name, MonitorMode *obj, Error **errp)
{
    int value = *obj;
    visit_type_enum(v, name, &value, &MonitorMode_lookup, errp);
    *obj = value;
}

void visit_type_MonitorOptions_members(Visitor *v, MonitorOptions *obj, Error **errp)
{
    Error *err = NULL;

    if (visit_optional(v, "id", &obj->has_id)) {
        visit_type_str(v, "id", &obj->id, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "mode", &obj->has_mode)) {
        visit_type_MonitorMode(v, "mode", &obj->mode, &err);
        if (err) {
            goto out;
        }
    }
    if (visit_optional(v, "pretty", &obj->has_pretty)) {
        visit_type_bool(v, "pretty", &obj->pretty, &err);
        if (err) {
            goto out;
        }
    }
    visit_type_str(v, "chardev", &obj->chardev, &err);
    if (err) {
        goto out;
    }

out:
    error_propagate(errp, err);
}

void visit_type_MonitorOptions(Visitor *v, const char *name, MonitorOptions **obj, Error **errp)
{
    Error *err = NULL;

    visit_start_struct(v, name, (void **)obj, sizeof(MonitorOptions), &err);
    if (err) {
        goto out;
    }
    if (!*obj) {
        goto out_obj;
    }
    visit_type_MonitorOptions_members(v, *obj, &err);
    if (err) {
        goto out_obj;
    }
    visit_check_struct(v, &err);
out_obj:
    visit_end_struct(v, (void **)obj);
    if (err && visit_is_input(v)) {
        qapi_free_MonitorOptions(*obj);
        *obj = NULL;
    }
out:
    error_propagate(errp, err);
}

/* Dummy declaration to prevent empty .o file */
char qapi_dummy_qapi_visit_control_c;
