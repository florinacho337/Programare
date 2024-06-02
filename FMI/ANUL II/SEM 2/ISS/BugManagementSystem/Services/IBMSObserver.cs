using Model;

namespace Services;

public interface IBmsObserver
{
    void BugAdded(Bug bugREntity);
    void BugUpdated(Bug newBug);
    void BugRemoved(Bug newBug);
}