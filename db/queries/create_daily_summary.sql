create table daily_summary (
  id bigint generated by default as identity primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  ticker_id integer,
  close float,
  high float,
  low float,
  open float,
  timestamp timestamp,
  volume integer,
  constraint fk_ticker
  foreign key (ticker_id) references tradeable_asset(id)
);