<%inherit file="base.mako" />

<%def name="body()">
<p>This page is private for authenticated users!</p>
<h2>All registered users</h2>
<ul>
  % for user in all_users:
    <li>${user.username}</li>
  % endfor
</ul>
</%def>
