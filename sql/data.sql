begin;

insert into piggybank.user values (default, 'administrator@email.com', '153417bd132637ba71cf236c323a55bd', '71a8b28bf9986f51ab5e31c1c20993f3', 'admin', 'piggybank', 'admin');
insert into piggybank.user values (default, 'employee@email.com', '153417bd132637ba71cf236c323a55bd', '71a8b28bf9986f51ab5e31c1c20993f3', 'employee', 'piggybank', 'employee');
insert into piggybank.user values (default, 'customer1@email.com', '153417bd132637ba71cf236c323a55bd', '71a8b28bf9986f51ab5e31c1c20993f3', 'customer1', 'piggybank', 'active');
insert into piggybank.user values (default, 'customer2@email.com', '153417bd132637ba71cf236c323a55bd', '71a8b28bf9986f51ab5e31c1c20993f3', 'customer2', 'piggybank', 'active');

insert into piggybank.account values (default, 'debit', 10.00);
insert into piggybank.account values (default, 'credit', 10.00);

insert into piggybank.user_account values (default, 3, 1);
insert into piggybank.user_account values (default, 4, 2);

commit;
