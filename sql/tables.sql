begin;

create schema piggybank;

create table piggybank.user (
	id serial unique primary key,
	email varchar(200) unique,
	pass_hash varchar(200),
	pass_salt varchar (200),
	first_name varchar(50),
	last_name varchar(200),
	status varchar(50) 
		check ((status = 'employee')
		or (status = 'admin')
		or (status = 'active')
		or (status = 'pending credit')
		or (status = 'pending debit')
		or (status = 'closed'))
);

create table piggybank.account (
	id serial unique primary key,
	account_type varchar(50) check (account_type = 'debit' or account_type = 'credit'),
	balance numeric check ((account_type = 'debit' and balance >= 0.00) or (account_type = 'credit'))
);

create table piggybank.user_account (
	id serial unique primary key,
	user_id int not null,
	account_id int not null,
	foreign key (user_id) references piggybank.user(id) on delete cascade,
	foreign key (account_id) references piggybank.account(id)
);

create table piggybank.transaction (
	id serial unique primary key,
	source_account_id int not null,
	source_user_id int not null,
	transfer_amount numeric not null,
	destination_account_id int,
	transaction_time timestamptz DEFAULT current_timestamp,
	foreign key (source_account_id) references piggybank.account(id),
	foreign key (source_user_id) references piggybank.user(id),
	foreign key (destination_account_id) references piggybank.account(id)
);

commit;
