from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.modules.personal import personal_bp
from app.modules.personal.forms import PersonalRecordForm
from app.modules.personal.models import PersonalRecord
from app import db
from app.utils import is_blueprint_active

@personal_bp.route('/records', methods=['GET', 'POST'])
@login_required
def manage_records():
    form = PersonalRecordForm()
    if form.validate_on_submit():
        record = PersonalRecord(
            type=form.type.data,
            name=form.name.data,
            dob=form.dob.data,
            ssn=form.ssn.data,
            account_number=form.account_number.data,
            account_type=form.account_type.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(record)
        db.session.commit()
        flash('Record added successfully!', 'success')
        return redirect(url_for('personal.manage_records'))
    
    records = PersonalRecord.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_records.html', form=form, records=records)

@personal_bp.route('/record/delete/<int:id>', methods=['POST'])
@login_required
def delete_record(id):
    record = PersonalRecord.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully!', 'success')
    return redirect(url_for('personal.manage_records'))

@personal_bp.route('/record/edit/<int:id>', methods=['POST'])
@login_required
def edit_record(id):
    record = PersonalRecord.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = PersonalRecordForm()
    
    if form.validate_on_submit():
        record.type = form.type.data
        record.name = form.name.data
        record.dob = form.dob.data
        record.ssn = form.ssn.data
        record.account_number = form.account_number.data
        record.account_type = form.account_type.data
        record.notes = form.notes.data
        
        db.session.commit()
        flash('Record updated successfully!', 'success')
        
    return redirect(url_for('personal.manage_records'))

@personal_bp.route('/personal_dashboard')
@login_required
def personal_dashboard():
    """Personal dashboard with integrated views from finance and health."""
    # Get finance data
    accounts = []
    transactions = []
    if is_blueprint_active('finance'):
        from app.modules.finance.models import Account, Transaction
        accounts = Account.query.filter_by(user_id=current_user.id).all()
        transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(5).all()
    
    # Get health data
    health_records = []
    if is_blueprint_active('health_tracker'):
        from app.modules.health.models import HealthRecord
        health_records = HealthRecord.query.filter_by(
            user_id=current_user.id
        ).order_by(HealthRecord.date.desc()).limit(5).all()
    
    # Get personal records
    personal_records = PersonalRecord.query.filter_by(user_id=current_user.id).limit(5).all()
    
    return render_template(
        'personal_dashboard.html',
        accounts=accounts,
        transactions=transactions,
        health_records=health_records,
        tasks=[],  # Empty list for backward compatibility with template
        personal_records=personal_records,
        is_blueprint_active=is_blueprint_active
    )
