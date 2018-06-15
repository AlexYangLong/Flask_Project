from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_restful import Resource, reqparse

from bms.models import Admin
from utils.decorators import login_required
from utils.exts import api