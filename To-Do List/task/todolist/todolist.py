#Author: Aleksandra Aramian
#Code: ToDoList

from sqlalchemy import create_engine
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

import sys
from exitstatus import ExitStatus

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.today()


def menu():
    menu_options = ["1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Missed tasks",
                    "5) Add task", "6) Delete task", "0) Exit"]
    for value in menu_options:
        print(value)
    menu_answer()


def today_task():
    all_tasks = session.query(Table).filter(Table.deadline == today.date())
    if all_tasks.count() > 0:
        print(f"Today {today.day} {today.strftime('%b')}:")
        for task in all_tasks:
            print(task.task)
    else:
        print(
            'Today:', 'Nothing to do!', sep='\n' )
    print()
    menu()


def add_task():
    print('Enter task')
    user_task_input = input()
    print('Enter deadline')
    user_date_input = datetime.strptime(input(), '%Y-%m-%d')

    session.add(Table(task=user_task_input,
                  deadline=user_date_input.date()))
    session.commit()
    print('The task has been added! \n')
    menu()


def missed_task():
    print('Missed tasks:')
    rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < today.date()).all()
    if rows:
        for idx, value in enumerate(rows, start=1):
            print('{}. {}. {} {}'.format(idx, value.task, value.deadline.day, value.deadline.strftime('%b')))
    else:
        print('Nothing is missed!')
    print()
    menu()



def delete_task():
    whole_db = session.query(Table).order_by(Table.deadline).all()
    print('Choose the number of the task you want to delete:')
    show_all_tasks()
    user_input = int(input())
    if user_input <= len(whole_db) and whole_db:
        session.delete(whole_db[user_input-1])
        session.commit()
        print('The task has been deleted! \n')
    elif not whole_db:
        print('Nothing to delete \n')
    elif user_input>len(whole_db):
        print('Wrong input \n')


def all_tasks():
    whole_db = session.query(Table).order_by(Table.deadline).all()
    if not whole_db:
        print('Today {} {}: \n Nothing to do!'.format(today.day, today.strftime('%b')))
        print()
    else:
        print('All tasks:')
        return show_all_tasks()
        print()
    menu()

def show_all_tasks():
    whole_db = session.query(Table).order_by(Table.deadline).all()
    for idx, value in enumerate(whole_db, start=1):
        print('{}. {}. {} {}'.format(idx, value.task, value.deadline.day, value.deadline.strftime('%b')))
    print()


def week_tasks():
    for i in range(7):
        current_day = today + timedelta(days=i)
        print('{} {} {}:'.format(current_day.strftime('%A'), current_day.day, current_day.strftime('%b')))
        all_tasks = session.query(Table).order_by(Table.deadline).filter(Table.deadline == current_day.date())
        if all_tasks.count() > 0:
            for i, task in enumerate(all_tasks, start=1):
                print(f'{i}. {task.task} \n')
        else:
            print('Nothing to do!',  sep='\n' )
            print()

    menu()



def menu_answer():
    answer = int(input())
    if answer==0:
        print('Bye!')
        sys.exit(ExitStatus.success)
    elif answer==1:
        today_task()
    elif answer==2:
        week_tasks()
    elif answer==3:
        all_tasks()
    elif answer==5:
        add_task()
    elif answer==4:
        missed_task()
    elif answer==6:
        delete_task()
    else:
        print("Wrong input")
    menu()


menu()