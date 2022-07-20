Feature: Survey management
    As a system administrator
    I want to manage surveys
    So that I can solicit users' feedback

    Scenario: Survey is created from question group
        Given a valid system JWT
        And there exists a question group
        And a new FREE_TEXT question is created
        When a new survey is created
        Then the survey can be seen in all surveys
        And the survey can be retrieved by its uuid
        And the retrieved survey matches that previously posted


      
