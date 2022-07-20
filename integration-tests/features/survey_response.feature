Feature: Survey responses
    As a patient
    I want to reply to surveys
    So that I can provide my feedback when requested

    Background:
        Given a valid system JWT
        And there exists a question group
        And a new FREE_TEXT question is created
        And a new INTEGER question is created
        And a new CHECKBOX question is created
        And a new RADIO question is created
        And a new DROPDOWN question is created
        And a new RANGE question is created
        And a new survey is created


    Scenario: Patient responds to all answers in the survey
        Given a valid patient JWT
        And the survey can be retrieved by its uuid
        When all the answers to the survey are provided
        Then the submitted answers can be seen in all answers for that survey


        
