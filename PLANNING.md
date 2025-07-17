# Planning

## High level overview
Jambi is a headless CMS that makes it easy to create super fast static websites. The user can create their own templates in html/css/javascript and add placeholders with curly brackets (`{ }`) to have Jambi fill in the content as configured in the database schema. In a later stage, we'll build functionality so that a user can define their own schema using the UI. 

For now we want to have a simple UI where a user has an overview of which pages have been generated and the functionality to edit or delete these pages, as well as to create new ones.

The content that users write should be translated to Markdown and stored in the `content` field of our database. When it is time to generate the pages, we fetch this content and translate it into html that can be fed into the template.

## Architecture
The overall architecture should stay as simple as possible. The repository package handles everything that has to do with the database. The server contains all logic that has to do with serving the UI, as well as the UI components themselves.

The rendering package is used for rendering all the content that is created by users into the templates. This should be done safely, rapidly, and with as little errors as possible. If it does happen that some content can't be parsed because of wrong input, we want to be as verbose as possible as to why something doesn't work, to make sure to give the user a useful hint as to what should be fixed.

For the parsing of user input to Markdown in the content field of the database, we will create a new package called `parsing` which will contain logic to parse user input in the free format content field to Markdown. In the future we will need to extend this to more free format fields, as compared to normal text fields as for example "file_name".

## Testing
The current project contains multiple unit tests, covering the main codepaths in the backend. It's essential that we maintain the unit test suite, keeping high code coverage. We could add a couple integration tests that will make sure everything keeps working together. This will help us feel confident that new features don't have unintended consequences for the existing features. It's also important that when we implement new features, we write tests for them and fix existing tests that will fail because of our change if needed.