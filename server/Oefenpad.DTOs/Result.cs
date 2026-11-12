namespace Oefenpad.DTOs;

public sealed class Result<T>
{
    public T? ResultContent { get; set; }

    public bool IsSuccess { get; set; }

    public List<ResultMessage> Messages { get; } = [];

    public static Result<T> Success(T content) => new()
    {
        IsSuccess = true,
        ResultContent = content
    };

    public static Result<T> Failure(params ResultMessage[] messages)
    {
        var result = new Result<T>();
        result.Messages.AddRange(messages);
        return result;
    }
}
