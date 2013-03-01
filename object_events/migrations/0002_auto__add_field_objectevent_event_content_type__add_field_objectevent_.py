# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ObjectEvent.event_content_type'
        db.add_column('object_events_objectevent', 'event_content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='event_objects', null=True, to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'ObjectEvent.event_object_id'
        db.add_column('object_events_objectevent', 'event_object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'ObjectEvent.object_id'
        db.alter_column('object_events_objectevent', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'ObjectEvent.user'
        db.alter_column('object_events_objectevent', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ObjectEvent.content_type'
        db.alter_column('object_events_objectevent', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['contenttypes.ContentType']))

    def backwards(self, orm):
        # Deleting field 'ObjectEvent.event_content_type'
        db.delete_column('object_events_objectevent', 'event_content_type_id')

        # Deleting field 'ObjectEvent.event_object_id'
        db.delete_column('object_events_objectevent', 'event_object_id')


        # User chose to not deal with backwards NULL issues for 'ObjectEvent.object_id'
        raise RuntimeError("Cannot reverse this migration. 'ObjectEvent.object_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ObjectEvent.user'
        raise RuntimeError("Cannot reverse this migration. 'ObjectEvent.user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ObjectEvent.content_type'
        raise RuntimeError("Cannot reverse this migration. 'ObjectEvent.content_type' and its values cannot be restored.")

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'object_events.objectevent': {
            'Meta': {'object_name': 'ObjectEvent'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_content_objects'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event_objects'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'event_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['object_events.ObjectEventType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'object_events.objecteventtype': {
            'Meta': {'object_name': 'ObjectEventType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['object_events']
