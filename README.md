# api_yamdb

<p> REST API for YaMDb servise - movie, book and music reviews database. Team project of Practicum students by Yandex </p>

<h3>API for YaMDb service allows to run the following functions:</h3>

<ul>
    <li><b>Reviews</b>
        <ul>
            <li>Get a list of all reviews;</li>
            <li>Create a new review. User may post only one review per object;</li>
            <li>Get a review by id;</li>
            <li>Partially update the review by id;</li>
            <li>Delete review by id.</li>
        </ul>
    </li>
    <li><b>Comments</b>
        <ul>
            <li>Get a list of all comments to the review by id;</li>
            <li>Create a new comment for the review;</li>
            <li>Get a comment for a review by id;</li>
            <li>Partially update the comment on the review by id;</li>
            <li>Delete a comment to the review by id.</li>
        </ul>
    </li>
    <li><b>Auth</b>
        <ul>
            <li>Getting a JWT token in exchange for email and confirmation_code;</li>
            <li>Sending confirmation_code to the email.</li>
        </ul>
    </li>    
    <li><b>Users</b>
        <ul>
            <li>Get a list of all users;</li>
            <li>Create an user;</li>
            <li>Get user by username;</li>
            <li>Change user data by username;</li>
            <li>Delete user by username;</li>
            <li>Get personal account details;</li>
            <li>Change the personal account details</li>
        </ul>
    </li>
    <li><b>Categories</b>
        <ul>
            <li>Get a list of all categories;</li>
            <li>Create a category;</li>
            <li>Delete a category.</li>
        </ul>
    </li>
    <li><b>Genres</b>
        <ul>
            <li>Get a list of all genres;</li>
            <li>Create a genre;</li>
            <li>Delete a genre.</li>
        </ul>
    </li>
    <li><b>Titles</b>
        <ul>
            <li>Get a list of all titles;</li>
            <li>Create an title for reviews;</li>
            <li>Get title information;</li>
            <li>Update title information;</li>
            <li>Delete title.</li>
        </ul>
    </li>
</ul>


<p>Redoc Documentation - <a href="https://github.com/olifirovai/api_yamdb/blob/master/static/redoc_en.yaml">English version</a> and <a href="https://github.com/olifirovai/api_yamdb/blob/master/static/redoc_ru.yaml">Russian version</a></p>
<p></p>


<h5>Participants</h5>
<p><a href="https://github.com/JackDaniels07">Denis</a> - Content Part (reviews, comments, categories, genres, titles): Models, views, endpoints, permissions related to part, rating score</p>
<p><a href="https://github.com/olifirovai">Irina Olifirova</a> - User and Auth parts: registration and authentication, permissions, roles, token authentication, e-mail confirmation system.</p>
