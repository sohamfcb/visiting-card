create table details(
    name varchar(100),
    company varchar(200),
    address text,
    phone varchar(50),
    email varchar(100),
    website varchar(255)
);

select * from details;

alter table details add constraint check_unique unique (name,email);

# alter table details
# modify column phone varchar(50);

# alter table details
# drop constraint check_unique;

desc details;


alter table details
add column phone2 varchar(50) after phone;

alter table details
add column job_role varchar(100) after company;

select *
from details;

# delete from details;

alter table details
modify column phone2 varchar(50);

desc details;