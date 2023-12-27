def undo_service(lst, undolist):
    '''
    modifica lista actuala lst cu lista veche undolist
    :param lst: list
    :param undolist: list
    :return: - (modifica lista actuala lst cu lista veche undolist)
    '''
    if undolist == []: raise ValueError("Nu se mai poate da undo!")
    lst[:] = undolist[-1]
    undolist[:] = undolist[:-1]
