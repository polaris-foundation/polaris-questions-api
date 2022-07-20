Feature: Question management
    As a system administrator
    I want to manage questions
    So that I can build surveys

    Scenario Outline: New question is created
        Given a valid system JWT
        When a new <type> question is created
        Then the question can be retrieved by its uuid
        And the retrieved question matches that previously posted

        Examples:
            | type      |
            | FREE_TEXT |
            | INTEGER   |
            | CHECKBOX  |
            | RADIO     |
            | DROPDOWN  |
            | RANGE     |
    
    
    Scenario: Admin creates new question type
        Given a valid system JWT
        And a new question type is created
        When a new question is created from the custom question type
        Then the question can be retrieved by its uuid
